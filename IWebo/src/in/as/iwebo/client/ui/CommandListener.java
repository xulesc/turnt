package com.as.iwebo.client.ui;

/**
 * The interface to be implemented by any class that is required to listen
 * to the shell for new commands entered by the user.
 * 
 * @author anuj
 */
public interface CommandListener{
    public void commandAdded( final String cmd );
}
