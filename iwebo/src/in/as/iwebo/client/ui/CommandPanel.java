/*
 * Author: anuj sharma <anuj.sharma80@gmail.com>, (C) 2008
 *
 * Copyright: See COPYING file that comes with this distribution
 *
*/
package com.as.iwebo.client.ui;

import com.google.gwt.user.client.ui.DockPanel;
import com.google.gwt.user.client.ui.Widget;
import com.google.gwt.user.client.ui.Label;

public class CommandPanel extends DockPanel{

	public CommandPanel( Widget editor ){
            super();
            setStyleName("cmdWinFrame");
            DockPanel title = new DockPanel();
            title.add(new Label("Command Window"), DockPanel.WEST );
            add(title, DockPanel.NORTH);
            add(editor, DockPanel.CENTER);
	}

}
