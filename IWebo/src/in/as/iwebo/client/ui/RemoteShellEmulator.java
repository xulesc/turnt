package com.as.iwebo.client.ui;

import com.google.gwt.user.client.Event;
import com.google.gwt.user.client.Window;

import com.google.gwt.user.client.ui.Widget;
import com.google.gwt.user.client.ui.KeyboardListener;

import com.google.gwt.user.client.rpc.AsyncCallback;

import com.as.iwebo.client.services.RemoteSupportAsync;
import com.as.iwebo.client.LanguageParms;

import java.util.List;
import java.util.Collections;
import java.util.Map;
import java.util.HashMap;
import java.util.Arrays;

/**
 *
 * @author anuj
 */
public class RemoteShellEmulator extends AbstractShell {
    /**
     * handle to the remote service access object.
     */
    private RemoteSupportAsync service;

    public RemoteShellEmulator(RemoteSupportAsync service, boolean showLineNo) {
        super("ComWin.html","eFrameClass","editorFrame","editor","editorClass");
        this.service = service;
        setShowLineNum(showLineNo);
    }

    /**
     * The method is called when the client element have been completely 
     * intialized (see super class documentation for details). A call is made 
     * using the service handler to obtain Language data for octave which is 
     * required for code highlight on the client side as well as a list of 
     * commands that indicate begining to code blocks.
     * 
     * If in the future client side code block handling is deprecate the block
     * start lists will also be deprecated.
     */
    public void init() {
        service.getLanguageParms(new AsyncCallback() {
            public void onFailure(Throwable c) {
                Window.alert("Failed to get language parms: " + c.toString());
            }

            public void onSuccess(Object arg0) {
                LanguageParms lp = (LanguageParms) arg0;
                setHighlightMap(lp.getLangMap());
                setPrompt(lp.getPromptPre(), lp.getPromptSuf());
                blockStart = lp.getBlockStart();
                blockEnd = lp.getBlockEnd();
                initRemoteSupport();
            }
        });
    }

    /**
     * The method is called on receiving a successfull response for the service
     * call in init method. The method causes the intialization of the remote
     * octave handler.
     */
    private void initRemoteSupport() {
        service.initEngine(new AsyncCallback() {
            public void onFailure(Throwable caught) {
                Window.alert("Failed to initialize: " + caught.toString());
            }

            public void onSuccess(Object arg0) {
                prompt = promptPre + ":%s" + promptSuf;
                setCode(getPrompt());
            }
        });
    }
    
    /**
     * The method is called on any DOM events in the editor frame (see super
     * class documentation for details). 
     * 
     * Event handling is currently limited to KeyPress events. This will be
     * expanded in the future to mouse event handling as well.
     * 
     * @param evt DOM event
     */
    @Override
    public void onBrowserEvent(Event evt) {
        switch (evt.getTypeInt()) {
            case Event.ONCLICK:
                break;
            case Event.FOCUSEVENTS:
                break;
            case Event.ONKEYPRESS:
                int kcode = evt.getKeyCode();
                boolean mods = evt.getAltKey() || evt.getCtrlKey() || evt.getShiftKey();
                keyHandler(null, kcode, mods);
                break;
            case Event.ONKEYDOWN:
                evt.preventDefault();
                return;
            case Event.ONKEYUP:
                evt.preventDefault();
                return;
            default:
                return;
        }
    }
    /**
     * All key events handled by the shell are forwarded here on being received
     * by the onBrowserEvente method.
     * 
     * A lot of work needs to be done on supporting more key combinations here.
     * 
     * @param sender Widget sending widget (DEPRECATED)
     * @param keyCode int the ascii value of the key pressed
     * @param modifiers boolean true if Alt, Ctl or Shift key was pressed
     */
    protected void keyHandler(Widget sender, int keyCode, boolean modifiers) {
        String code = getCode();
        final int i = code.lastIndexOf(promptSuf) + 1;
        if (!modifiers && keyCode == KeyboardListener.KEY_ENTER) {
            addToHistory(code.substring(i, code.length()));
            evaluate(code);
            return;
        } else if (!modifiers && keyCode == KeyboardListener.KEY_BACKSPACE) {
            if (!code.endsWith(promptSuf)) {
                code = code.substring(0, code.length() - 1);
            }
        } else if (!modifiers && keyCode == KeyboardListener.KEY_UP) {
            code = code.substring(0, i) + getPreviousCmd();
        } else if (!modifiers && keyCode == KeyboardListener.KEY_DOWN) {
            code = code.substring(0, i) + getNextCmd();
        } else if (!modifiers && (keyCode == KeyboardListener.KEY_LEFT ||
                keyCode == KeyboardListener.KEY_RIGHT ) ) {
            return;
        } else {
            code += (char) keyCode;
        }
        setCode(code);
    }

    /**
     * The method is called by the keyHandler method.
     * 
     * The current command is retrieved from the command stack. If the command
     * indicated a block start the command will not be submitted to the server
     * instead a block command store is intialized. If the command contains a 
     * command stop word the block command store is updated. If the command 
     * block store returns incomplete then no processing is preformed otherwise
     * the entire block of command is setup to be sent to the server as a 
     * string.
     * 
     * If no block command store exists then the command (this may be the block
     * command string) is sent to the server for asynchronus execution. A hook
     * is attached to send the server response to the editor shell to be 
     * displayed to the user.
     * 
     * @param code String the current code in the editor
     */
    protected void evaluate(final String code) {
        String cmd = getCommand();
        if (hasBlockStart(cmd)) {
            cmdBlock = (cmdBlock == null) ? new CmdBlockStore() : cmdBlock;
            cmdBlock.addStopWord(cmd.replaceAll(blockStart, blockEnd));
        }
        if (cmdBlock != null && hasBlockStop(cmd)) {
            cmdBlock.removeStopWord();
            if (cmdBlock.isComplete()) {
                cmdBlock.addCommand(cmd);
                cmd = cmdBlock.toString();
                cmdBlock = null;
            }
        }
        if (cmdBlock != null) {
            cmdBlock.addCommand(cmd);
            setCode(code + "\n" + getPromptSuffix());
            return;
        }
        service.eval(cmd, new AsyncCallback() {

            public void onFailure(Throwable caught) {
                Window.alert("Failed to evaluate: " + caught.toString());
                setCode(code + "\r\n" + getPrompt());
            }

            public void onSuccess(Object arg0) {
                String s = (String) arg0;
                setCode(code + "\r\n" + s + getPrompt());
            }
        });
    }

    /**
     * The HTML tag removal regular expression map & the java string markup
     * replacement with HTML Tag are initialized here. These maps are used
     * extensively while getting and setting code to and from the editors HTML
     * element.
     */
    static {
        Map<String, String> t = new HashMap<String, String>();
        t.put("<br>", "\r\n");
        t.put("\\u2009", "\t");
        t.put("<P>", "\n");
        t.put("</P>", "\r");
        t.put("<.*?>", "");
        t.put("&nbsp;", "");
        t.put("&lt;", "<");
        t.put("&gt;", ">");
        t.put("&amp;", "&");
        inputModifier = Collections.unmodifiableMap(t);
        t = new HashMap<String, String>();
        t.put("\\r\\n", "<br>");
        t.put("\\r", "<br>");
        t.put("\\n", "<br>");
        outModifier = Collections.unmodifiableMap(t);
        //List<Integer> l = Arrays.asList(KeyboardListener.KEY_LEFT,
        //        KeyboardListener.KEY_RIGHT);
        //blockKeyList = l;
    }
}
