package com.as.iwebo.client.services;

import com.google.gwt.user.client.rpc.RemoteService;
import com.as.iwebo.client.LanguageParms;
/**
 * The interface that defines the various methods exported by the remote service
 * for this application.
 * 
 * @author anuj
 */
public interface RemoteSupport extends RemoteService {
    public void setLanguage(String lang);
    public LanguageParms getLanguageParms();
    public void initEngine();
    public String eval(String cmd);
}

