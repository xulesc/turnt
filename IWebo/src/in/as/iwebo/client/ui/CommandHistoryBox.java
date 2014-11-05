package com.as.iwebo.client.ui;

import com.google.gwt.user.client.ui.Widget;
import com.google.gwt.user.client.ui.ListBox;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.ChangeListener;

/**
 * A GUI element that displays the command history of the user for the session.
 * It extends a list box and takes a handle to the shell which is to be notified
 * if the user selection.
 * 
 * @author anuj
 */
public class CommandHistoryBox extends ListBox implements CommandListener{
    /**
     * handler to the shell that must be called with a user selection of 
     * command.
     */
    private RemoteShellEmulator cw = null;
    public CommandHistoryBox( boolean b ){
        super( b );
        addChangeListener( new ChangeListener(){
            public void onChange(Widget sender){
                selectionChanged();
            }		
        } );
    }
    public void associateShell(final RemoteShellEmulator r){
        cw = r;
    }
    
    /**
     * This method is called by the source of commands to be displayed in the
     * list.
     * 
     * @param cmd String the command to be added
     */
    public void commandAdded( final String cmd ){
        this.addItem( cmd );
    }
    public void selectionChanged(){
        if( cw == null ) Window.alert( "No shell found" );
        cw.runHistoryCommand( getItemText( getSelectedIndex() ) );
    }
}	
