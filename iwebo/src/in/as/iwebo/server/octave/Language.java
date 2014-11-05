package com.as.iwebo.server.octave;

import java.util.Map;
import java.util.HashMap;

/**
 * Class containing static language definition strings for octave.
 * 
 * @author anuj
 */
public class Language{
	public static String keywords = "\\b(function|endfunction|switch"+
	"|case|endswitch|otherwise|unwind_protect|unwind_protect_cleanup"+
	"|end_unwind_protect|try|catch|end_try_catch|end|if|else|elseif"+
	"|endif|break|continue|for|endfor|return|do|until|while|endwhile"+
	"|global|nargin|nargout|assert)\\b"; 
	public static String keywordsOut = "<k>$1</k>";

	public static String functions = "\\b(size|zeros|ones|min|max|varargs"+
	"|sqrt|atan2|asin|acos|log10|log|real|error|isscalar|isstr|strcmp|log2"+
	"|Inf|isvector|strcat|fsolve|islogical|isempty|isnumeric|prod|round"+
	"|dims|cumprod|ismatrix|floor|sort|ceil|linspace|isnan|isinf|nan_inf"+
	"|repmat|colums|rows|sum|rem|reshape|conv|length|usage|log2|abs|setstr"+
	"|printf|sprintf|fprintf|fread|fopen|fclose|system|unlink|error"+
	"|warning)\\b";
	public static String functionsOut = "<f>$1</f>";
	
	public static String reservedConstants = "\\b(pi|eps|inf|nan|NaN)\\b";
	public static String reservedConstantsOut = "<r>$1</r>";

	public static String singleLineComment = "(#|%.*)";
	public static String slcOut = "<c>$1</c>"; 

	public static String singleQuotedString = "\'(.*?)(\'|<br>|</P>)";
	public static String sqcOut = "<qs>\'$1$2</qs>"; 
	
	public static String doubleQuotedString = "\"(.*?)(\"|<br>|</P>)";
	public static String dqcOut = "<qs>\"$1$2</qs>"; 

	public static String multiLineComment = "(/\\*(?:.|[\\n\\r])*?\\*/)";
	public static String mlcOut = "<c>$1</c>";

	public static String blockStart = "\\b(function|switch|if|for|while)\\b(.*)";
	public static String blockStop = "end|end$1";

	public static Map<String,String> getLanguageMap(){
		Map<String,String> hmap = new HashMap<String,String>();
		hmap.put(keywords,keywordsOut);hmap.put(functions,functionsOut);
		hmap.put(reservedConstants,reservedConstantsOut);
		hmap.put(singleLineComment,slcOut);hmap.put(singleQuotedString,sqcOut);
		hmap.put(doubleQuotedString,dqcOut);hmap.put(multiLineComment,mlcOut);
		return hmap;
	}
}
	//@ToDO: figure out regexp for seperating ' of transpose as starting of
	//		single quoted string
    /*<context id="decimal" style-ref="decimal">
      <match>\b([1-9][0-9]*|0)([Uu]([Ll]|LL|ll)?|([Ll]|LL|ll)[Uu]?)?\b</match>
    </context>

    <context id="floating-point-number" style-ref="floating-point">
      <match>\b([0-9]+[Ee][-]?[0-9]+|([0-9]*\.[0-9]+|[0-9]+\.)([Ee][-]?[0-9]+)?)[fFlL]?</match>
    </context>

    <context id="octal-number" style-ref="base-n-integer">
      <match>\b0[0-7]+([Uu]([Ll]|LL|ll)?|([Ll]|LL|ll)[Uu]?)?\b</match>
    </context>

    <context id="hex-number" style-ref="base-n-integer">
      <match>\b0[xX][0-9a-fA-F]+([Uu]([Ll]|LL|ll)?|([Ll]|LL|ll)[Uu]?)?\b</match>
    </context>*/
