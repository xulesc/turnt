package com.as.iwebo.server;

import com.as.iwebo.client.services.RemoteSupport;
import com.google.gwt.user.server.rpc.RemoteServiceServlet;

import com.as.iwebo.client.LanguageParms;
import com.as.iwebo.server.octave.*;

import java.io.IOException;
import java.util.concurrent.ExecutionException;
import java.util.logging.Level;

/**
 * The remote service implemenetation for the application.
 * 
 * @author anuj
 */
public class RemoteSupportImpl extends RemoteServiceServlet implements
        RemoteSupport {
    /**
     * Language for which the remote service will instantiate server side
     * objects. (Maybe we will be able to support more than one languages in the
     * future!!!)
     */
    private String language;
    private OctaveEngine engine;

    /**
     * Set the language for which shell was instantiated on the client.
     * 
     * @param lang String the language name
     */
    public void setLanguage(final String lang) {
        language = lang;
    }
    
    /**
     * Returns the language parameters that will be used on the client for 
     * syntax highlighting and other language related operations.
     * 
     * @return LanguageParms object containing the data
     */
    public LanguageParms getLanguageParms() {
        LanguageParms lp = new LanguageParms();
        lp.setLangMap(Language.getLanguageMap());
        lp.setBlockStart(Language.blockStart);
        lp.setBlockEnd(Language.blockStop);
        lp.setPromptPre(language);
        lp.setPromptSuf(">");
        return lp;
    }

    public void initEngine() {
        try {
            engine = new OctaveEngine();
        } catch (IOException ex) {
            log(Level.SEVERE.toString(), new Throwable(ex));
        }
    }
    
    /**
     * Executes the command on the server object.
     * 
     * @param cmd String containing the command to be executed
     * @return String the server process response to the execution.
     */
    public String eval(final String cmd) {
        try {
            return engine.evaluate(cmd);
        } catch (InterruptedException ex) {
            log(Level.SEVERE.toString(), new Throwable(ex));
        } catch (ExecutionException ex) {
            log(Level.SEVERE.toString(), new Throwable(ex));
        } catch (IOException ex) {
            log(Level.SEVERE.toString(), new Throwable(ex));
        }
        return null;
    }
}
