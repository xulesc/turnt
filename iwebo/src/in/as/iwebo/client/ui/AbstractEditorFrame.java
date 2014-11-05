package com.as.iwebo.client.ui;

import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.DOM;
import com.google.gwt.user.client.Element;
import com.google.gwt.user.client.Event;
import com.google.gwt.user.client.ui.Widget;

/**
 *
 * @author anuj
 */
public abstract class AbstractEditorFrame extends Widget {
    /**
     * the element contains a reference to the element that loads the page in 
     * which the actual code editing happens. the frame is set in debugmode 'on'
     * after load to allow the user to type in.
     */
    protected Element iframe;
    /**
     * indicates if the frame is loading and initializing. most  browsers take 
     * some time before the iframe is instantiated and the contained page 
     * document is available for editing.
     */
    private boolean initializing;
    /**
     * the HTML pre element in which the edited text is stored at run time. the 
     * element is created after the iframe page loads.
     */
    protected Element editor;
    /**
     * client browser type. used for differential Javascript processing
     */
    protected String userAgent;
    private String editorId;
    private String editorStyleClass;
    
    public AbstractEditorFrame( final String url, final String frameStyleClass,
            final String frameId, final String editorId, 
            final String editorStyleClass)
    {
        this.editorId = editorId;
        this.editorStyleClass = editorStyleClass;
        iframe = createElement();
        DOM.setElementAttribute(iframe, "id", frameId);
        setElement(iframe);
        setOnLoad( url,frameStyleClass );
    }
    
    public Element getFrame(){
        return iframe;
    }

    private native Element createElement()
    /*-{
        return $doc.createElement('iframe');
    }-*/;
    
    /**
     * Specify the frame source url and the class name. Add an onload method
     * for post load processing.
     *$wnd.onload
     * @param url the url of the page to be loaded
     * @param className the style class
     */    
    private native void setOnLoad( final String url,final String className )
    /*-{
        this.@com.as.iwebo.client.ui.AbstractEditorFrame::iframe.src = url;
        this.@com.as.iwebo.client.ui.AbstractEditorFrame::iframe.className = className;
        if( navigator.userAgent.match('Gecko') )
          $wnd.onload = this.@com.as.iwebo.client.ui.AbstractEditorFrame::initElement()();
        else 
          $wnd.addEventListener('DOMContentLoaded',this.@com.as.iwebo.client.ui.AbstractEditorFrame::initElement()(),false);
    }-*/;
    
    /**
     * Post frame page load initialization. Create the HTML 'PRE' element to be 
     * used as the editing area. Attach event listeners to the frame document
     * and set event forwarding to the 'onBrowserEvent' event handling function.
     * Exists with a call to the 'onElementInitialized' method indicating the
     * editor is ready to use.
     * 
     * The event listeners are added in this method because the Element object
     * of GWT does not provide an interface for adding event listeners. Attempts
     * to user the Frame GWT element did not yield expected results in terms of
     * designmode settings and event handlers. 
     * 
     * Future work perhaps give Frame element a closer look
     */
    private native void initElement()
    /*-{
        var _this = this;
        _this.@com.as.iwebo.client.ui.AbstractEditorFrame::initializing = true;
        var elem = _this.@com.as.iwebo.client.ui.AbstractEditorFrame::iframe;
        var _edId = _this.@com.as.iwebo.client.ui.AbstractEditorFrame::editorId;
        var _edClass = _this.@com.as.iwebo.client.ui.AbstractEditorFrame::editorStyleClass;
       	_this.@com.as.iwebo.client.ui.AbstractEditorFrame::userAgent = navigator.userAgent;

        setTimeout(function() {
            var _wnd = elem.contentWindow;
            _wnd.document.designMode = 'on';
            var _child = _wnd.document.createElement('pre');
            _child.id = _edId;
            _child.className = _edClass;
            _child.setVisible = 'visible';
            _wnd.document.body.appendChild( _child );
            _this.@com.as.iwebo.client.ui.AbstractEditorFrame::editor = _child;
            
            elem.__gwt_handler = function(evt) {
                if (elem.__listener) {
                    elem.__listener.@com.as.iwebo.client.ui.AbstractEditorFrame::onBrowserEvent(Lcom/google/gwt/user/client/Event;)(evt);
                }
            };
            _wnd.addEventListener('keydown', elem.__gwt_handler, true);
            _wnd.addEventListener('keyup', elem.__gwt_handler, true);
            _wnd.addEventListener('keypress', elem.__gwt_handler, true);
            //_wnd.addEventListener('click', elem.__gwt_handler, true);
            _wnd.addEventListener('mousedown', elem.__gwt_handler, true);
            _wnd.addEventListener('mouseup', elem.__gwt_handler, true);
            _wnd.addEventListener('mousemove', elem.__gwt_handler, true);
            _wnd.addEventListener('mouseover', elem.__gwt_handler, true);
            _wnd.addEventListener('mouseout', elem.__gwt_handler, true);
            //_wnd.addEventListener('focus', elem.__gwt_handler, true);
            //_wnd.addEventListener('blur', elem.__gwt_blurHandler, true);
            
            _this.@com.as.iwebo.client.ui.AbstractEditorFrame::onElementInitialized()();
        }, 200);
    }-*/;
        
    protected void onElementInitialized(){
        initializing = false;
        init();
    }
    
    /**
     * Extending classes are expected to implement this method and add any
     * additional client initialization that is needed. Note at the point where
     * this method is called the basic editor is fully intialized and the editor
     * area is available for use.
     */
    public abstract void init();

    /**
     * Alter the designmode of the frame. Call to this method alternates the
     * value of the editor containing frame between 'on' and 'off'.
     * 
     * @return String the current value of the frame designmode (after change).
     */
    public native String toggleDesignMode()
    /*-{
        var _wnd = this.@com.as.iwebo.client.ui.AbstractEditorFrame::iframe.contentWindow;
        var _dMode = _wnd.document.designMode;
        _wnd.document.designMode = ( _dMode.toLowerCase() == 'on' ) ? 'off' : 'on';
        return _wnd.document.designMode;
    }-*/;
    
    /**
     * Positions the cursor in the frame document where the first occurance of 
     * the string cc is found. The occurance is deleted and the cursor is 
     * positioned in its place. This is a neat trick that uses the find method
     * exported by the contentWindow of a frame!!! Note there is no way of
     * specifying coordinates for locating a cursor in a frame in designmode
     * (at least that i know of).
     * 
     * @param cc String used to find positioning coordinates
     */
    public native void positionCursor(final String cc)
    /*-{
        var _wnd = this.@com.as.iwebo.client.ui.AbstractEditorFrame::iframe.contentWindow;
	var _ua = this.@com.as.iwebo.client.ui.AbstractEditorFrame::userAgent;

        if(_ua.match('Gecko')){ 
		if(_wnd.find(cc))
            		_wnd.getSelection().getRangeAt(0).deleteContents();
	}else if(_ua.match('MSIE')){
		range = _wnd.document.body.createTextRange();
		if(range.findText(cc)){
			range.select();
			range.text = '';
	}}
     }-*/;
    
    /**
     * Extending classes are expected to implement this method and provide 
     * custom event handling. All DOM events in the editor frame are forwarded
     * to this method through hooks setup in 'initElement' method.
     * 
     * @param e DOM event
     */
    @Override
    public abstract void onBrowserEvent(Event e);
}
