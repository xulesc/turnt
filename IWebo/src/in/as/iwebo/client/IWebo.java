package com.as.iwebo.client;

import com.google.gwt.core.client.EntryPoint;
import com.google.gwt.user.client.ui.RootPanel;
import com.google.gwt.user.client.ui.DockPanel;
import com.google.gwt.user.client.ui.Label;
import com.google.gwt.user.client.ui.HasHorizontalAlignment;
import com.google.gwt.user.client.ui.HasVerticalAlignment;

import com.google.gwt.user.client.rpc.AsyncCallback;

import com.as.iwebo.client.services.AsyncServices;
import com.as.iwebo.client.services.RemoteSupportAsync;

import com.as.iwebo.client.ui.RemoteShellEmulator;
import com.as.iwebo.client.ui.CommandPanel;
import com.as.iwebo.client.ui.SupplementPanel;

import com.google.gwt.user.client.Window;

/**
 * Entry point classes define <code>onModuleLoad()</code>.
 */
public class IWebo implements EntryPoint {
	private RemoteSupportAsync service;
  	public void onModuleLoad() {
            service = AsyncServices.getRemoteSupport();
		service.setLanguage("octave",new AsyncCallback() {
        	public void onFailure(Throwable caught) {
          		Window.alert("Failed to initialize: " + caught.toString());
        	}

        	public void onSuccess(Object arg0) {
			doGUIInit();
                }
            });
  	}
	private void doGUIInit(){
                DockPanel app = new DockPanel();
                app.setStyleName("appFrame");

		DockPanel top = new DockPanel();
		top.setSize("100%","50px");
		DockPanel topInner = new DockPanel();
		topInner.setStyleName("appBanner");
		Label l = new Label("Web Octave Shell");
		l.setStyleName("titleText");
		topInner.add(l,DockPanel.WEST);
		top.add(topInner,DockPanel.CENTER);
		top.setCellHorizontalAlignment(topInner,HasHorizontalAlignment.ALIGN_CENTER);
		top.setCellVerticalAlignment(topInner,HasVerticalAlignment.ALIGN_MIDDLE);

        	final RemoteShellEmulator r = new RemoteShellEmulator(service,true);
                final SupplementPanel d = new SupplementPanel();
                r.addCommandListener( d.getHistoryBox() );
                d.getHistoryBox().associateShell( r );

                final DockPanel d1 = new CommandPanel( r );

		app.add(top,DockPanel.NORTH);
		app.add(d,DockPanel.WEST);
                app.add(d1,DockPanel.CENTER);

                app.setCellWidth(d,"30%");
                app.setCellWidth(d1,"70%");

		RootPanel.get().add( app );
	}
}
