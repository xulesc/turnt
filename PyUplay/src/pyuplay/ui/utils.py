

def set_button_width(button):
	textWidth = button.fontMetrics().boundingRect(button.text()).width()
	button.setMaximumWidth(textWidth + 15) 

def add_widgets_to_component(component=None, widgets=[]):
	if component == None or widgets == None:
		return	
	for widget in widgets:
		component.addWidget(widget)

def extract_video_url(url_string):
	url_string = url_string.replace('watch', 'watch_popup')
	return url_string
