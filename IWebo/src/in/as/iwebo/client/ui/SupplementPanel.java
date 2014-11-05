/*
 * Author: anuj sharma <anuj.sharma80@gmail.com>, (C) 2008
 *
 * Copyright: See COPYING file that comes with this distribution
 *
*/
package com.as.iwebo.client.ui;

import com.google.gwt.user.client.ui.DockPanel;
import com.google.gwt.user.client.ui.ListBox;
import com.google.gwt.user.client.ui.Label;

import com.as.iwebo.client.ui.CommandHistoryBox;

public class SupplementPanel extends DockPanel{
	private CommandHistoryBox histBox;
	
	public SupplementPanel(){
            super();
            setStyleName("suppFrame");

            /*DockPanel session = new DockPanel();
            session.setStyleName("innerPanel");
            DockPanel sTitle = new DockPanel();
            sTitle.add(new Label("Session Variables"), DockPanel.WEST );
            session.add(sTitle, DockPanel.NORTH);
            ListBox l = new ListBox(true);
            l.setSize("100%","350px");
            session.add(l, DockPanel.CENTER);
            l.setEnabled(false);*/

            DockPanel cHist = new DockPanel();
            cHist.setStyleName("innerPanel");
            DockPanel cTitle = new DockPanel();
            cTitle.add(new Label("Command History"), DockPanel.WEST );
            cHist.add(cTitle, DockPanel.NORTH);
            histBox = new CommandHistoryBox(true);
            histBox.setSize("100%","700px");
            cHist.add(histBox, DockPanel.CENTER);

            //add(session, DockPanel.NORTH);
            add(cHist, DockPanel.CENTER);
	}

	public CommandHistoryBox getHistoryBox(){
		return histBox;
	}

}