package com.as.iwebo.client.ui;

import com.google.gwt.user.client.Event;

import java.util.List;
import java.util.ArrayList;
import java.util.Map;

/**
 *
 * @author anuj
 */
public abstract class AbstractShell extends AbstractEditorFrame{
    /**
     * map used for modifying html tags to java string equivalents or removing
     * them entirely when getting code from the editor for forwarding to the
     * code processing backend and syntax highlighting. the map is expected to
     * be supplied by the extending class.
     */
    protected static Map <String,String> inputModifier;
    /**
     * map used for modifying java string markups to html tags while putting 
     * code back to the editor after code processing or syntax highlighting. the
     * map is expected to be filled by the extending class.
     */
    protected static Map <String,String> outModifier;
    /**
     * prompt prefix to be displayed in the command shell.
     */
    protected String promptPre;
    /**
     * prompt suffix to be displayed in the command shell.
     */
    protected String promptSuf;
    /**
     * actual prompt string displayed in the shell. it is created by a 
     * concatenation of propmptPre and promptSuf.
     */
    protected String prompt;
    /**
     * whether command line number is to be displayed in the prompt or not. its
     * default value is set to false by can be overridden by setting to true.
     */
    protected boolean showLineNumbers = false;
    /**
     * syntax highlighting map containg command strings as keys and the html
     * tagging regular expression as value. the map is expected to be supplied
     * by the extending class. the key - value pair are used for inline string
     * replacement that converts a non-highlighted stream of strings to a 
     * HTML tagged string stream that should result in highlighting provided the
     * displaying page contains the HTML tag with an appropriate color specified
     * for the font.
     */
    protected Map<String,String> highlightMap;
    /**
     * used for determining command to display while command history scroll
     * using the arrow keys.
     */
    protected int currCmd = 0;
    /**
     * list storing the command history for the session.
     */
    protected List<String> cmdHist = new ArrayList<String>();
    /**
     * the variable contains a reference to an object that stores the commands 
     * in a multi line block when the block is still open. see class reference
     * for details.
     */
    protected CmdBlockStore cmdBlock = null;
    protected String blockStart;
    protected String blockEnd;
    /**
     * list containing all external elements listening to this widget for
     * notification when a new command is entered by the user.
     */
    protected List<CommandListener> cmdListeners = 
                                    new ArrayList<CommandListener>();
    /**
     * caret value used for cursor positioning in the EditorFrame.
     */
    protected String caret = "\u2009";
    
    public AbstractShell(final String url, final String fClass, 
        final String fId, final String editorId, final String eClass){
        super(url,fClass,fId,editorId,eClass);
    }
    /**
     * see super class documentation for the method.
     */
    public abstract void init();
    /**
     * see super class documentation for the method.
     * 
     * @param e DOM event.
     */
    public abstract void onBrowserEvent(Event e);
    /**
     * extending classes are expected to use this method to provide 
     * implementation of code evaluation to be performed on the code passed as
     * a parameter.
     * 
     * @param code String the code to be evaluated
     */
    protected abstract void evaluate(final String code);
    
    /**
     * Set the prompt prefix and suffix value for the instance.
     * 
     * @param p String containing prompt prefix desired
     * @param s String containing prompt suffix desired
     */
    public void setPrompt(final String p, final String s){ 
        promptPre = p; 
        promptSuf = s; 
    }
    
    /**
     * Set the highlighting map.
     * 
     * @param m Map with String key - value pairs
     */
    public void setHighlightMap(final Map<String,String> m){ 
        highlightMap = m; 
    }
    
    /**
     * Set boolean value indicating line numbers visible or not.
     * 
     * @param b boolean value of the showLineNumbers property.
     */
    public void setShowLineNum( final boolean b ){ 
        showLineNumbers = b; 
    }

    /**
     * Returns the last command entered by the user.
     * 
     * @return String last user command
     */
    public String getCommand(){
        return cmdHist.get(cmdHist.size()-1);
    }
    
    /**
     * Returns the prompt suffix being used in this instance.
     * 
     * @return String prompt suffix
     */
    public String getPromptSuffix(){
        return promptSuf;
    }
    
    /**
     * Adds a listener to the list of known Widgets listening for new commands
     * to this widget.
     * 
     * @param CommandListener l widget that is interested in listening
     */
    public void addCommandListener(final CommandListener l){
        cmdListeners.add( l );
    }
    
    /**
     * Utility method for running a command from the history store. The method
     * expects the history command to be passed to it. The action of the method
     * is to add the command to the command window at the current prompt. 
     * 
     * @param cmd String the command from history to be displayed
     */
    public void runHistoryCommand(final String cmd){
        setCode( getCode() + cmd );
    }

    /**
     * Retrieve code from the editor. The method processes the HTML string 
     * retrieved from the editor element removing all HTML tags and replacing
     * them as defined in the inputModifier map.
     * 
     * @return String current code in the editor element.
     */
    final protected String getCode(){
        String o = editor.getInnerHTML();
        for(String k : inputModifier.keySet() )
            o = o.replaceAll(k,inputModifier.get(k));
        return o;
    }
    
    /**
     * Sets code in the editor. The input code string is processed through the 
     * highlightMap to add all HTML tags required for syntax highlighting and 
     * them processed through the outModifier map to replace all java string
     * formating string with HTML formating tags.
     * 
     * @param code String the code to be set in the editor.
     */
    final protected void setCode(String code){
        for(String k : highlightMap.keySet())
            code = code.replaceAll(k,highlightMap.get(k));
        for(String k : outModifier.keySet() )
            code = code.replaceAll(k,outModifier.get(k));
        editor.setInnerHTML( code + caret );
        positionCursor( caret );
    }	
    
    /**
     * Returns the concatenated prompt string ensuring if line number show is on
     * the correct command line number is included.
     * 
     * @return String the prompt
     */
    final protected String getPrompt(){
        return prompt.replaceAll( "%s", 
                            ( showLineNumbers ) ? cmdHist.size() + 1 + "":"");
    }
    
    /**
     * Add a command to the history store list. It also calls all listeners with
     * the command entered as a parameter.
     * 
     * @param cmd String the new user command
     */
    final protected void addToHistory(final String cmd){
        cmdHist.add( cmd );
        for(CommandListener l : cmdListeners)
            l.commandAdded( cmd );
        currCmd = cmdHist.size();		
    }
    
    /**
     * Returns the previous command. Uses the currCmd as index to indicate where
     * we are in the history of commands to determine the command to return. It
     * returns the first command in the history block if we are at the top of
     * history store.
     * 
     * @return String previous command
     */
    final protected String getPreviousCmd(){
        return (currCmd<=0)?cmdHist.get(0):cmdHist.get(--currCmd );
    }
    
    /**
     * Returns the next command. Uses the currCmd as index to indicate where
     * we are in the history of commands to determine the command to return. It
     * returns a blank if we are at the end of the command history.
     * 
     * @return String next command
     */    
    final protected String getNextCmd(){
        return (currCmd>=cmdHist.size()-1)?"":cmdHist.get(++currCmd );
    }
    
    /**
     * Checks if string contains a block start command.
     * 
     * @param cmd the string to check
     * @return boolean indicating if the blockStart string was found or not
     */
    final protected boolean hasBlockStart(final String cmd){
        return !cmd.replaceAll(blockStart,"$1").equals(cmd);
    }
    
    /**
     * Checks if strinc contains a block stop command.
     * 
     * @param cmd the string to check
     * @return boolean indicating if the blockStop string was found or not
     */
    final protected boolean hasBlockStop(final String cmd){
        return !cmd.replaceAll(cmdBlock.getStopWord(),"").equals(cmd);
    }

    /**
     * The class is used to instantiate block objects whenever the user enters
     * a block code. The instantiated objects ensures that block is considered 
     * closed appropriately.
     * 
     * In future it would be useful to eliminate this entirely. Currently the
     * backend does not support entering block commands interactively.
     */
    protected class CmdBlockStore {
        /**
         * list storing the commands for this block of commands.
         */
        private List<String> commandQueue = new ArrayList<String>();
        /**
         * list used internally as a stack for ensuring blocks closings are
         * paired with appropriate block starts.
         */
        private List<String> blockStopStack = new ArrayList<String>();

        public void addCommand(final String cmd){
            commandQueue.add(cmd);
        }
        public void addStopWord(final String wrd){
            blockStopStack.add(wrd);
        }
        public String getStopWord(){
            return (blockStopStack.size()>0)?
                            blockStopStack.get(blockStopStack.size()-1):"";
        }
        /**
         * removes the top most block stop keyword on the stack.
         */
        public void removeStopWord(){
            blockStopStack.remove(blockStopStack.size()-1);
        }
        public boolean isComplete(){
            return blockStopStack.size()==0;
        }
        public List<String> getCommands(){return commandQueue;}
        @Override
        public String toString(){
            String ret = "";
            for(String s : commandQueue)
                ret += s + " ";
            return ret;
        }
    }
}
