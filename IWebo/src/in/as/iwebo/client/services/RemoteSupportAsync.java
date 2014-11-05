package com.as.iwebo.client.services;

import com.google.gwt.user.client.rpc.AsyncCallback;

/**
 * The interface that provides a wrapper for using the RemoteService without
 * blocking client.
 * 
 * @author anuj
 */
public interface RemoteSupportAsync {
    public void setLanguage(String lang,AsyncCallback asyncCallback);
    public void getLanguageParms(AsyncCallback asyncCallback);
    public void initEngine(AsyncCallback asyncCallback);
    public void eval(String cmd,AsyncCallback asyncCallback);
}

