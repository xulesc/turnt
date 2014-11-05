package com.as.iwebo.client.services;

import com.google.gwt.core.client.GWT;
import com.google.gwt.user.client.rpc.ServiceDefTarget;

/**
 * Class contains static method for generating a service handler for the
 * remote service(s) used in the application.
 * 
 * @author anuj
 */
public class AsyncServices {
    public static RemoteSupportAsync getRemoteSupport(){
        RemoteSupportAsync service = 
                (RemoteSupportAsync)GWT.create(RemoteSupport.class);
        ServiceDefTarget endpoint = (ServiceDefTarget) service;
        String moduleRelativeURL = GWT.getModuleBaseURL() + "/remoteSupport";
        endpoint.setServiceEntryPoint(moduleRelativeURL);
        return service;        
    }
}

