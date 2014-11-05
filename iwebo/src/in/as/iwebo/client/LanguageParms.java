package com.as.iwebo.client;

import java.util.Map;

/**
 * Data communication class between remote code and the client when the client
 * requests Language parameters.
 * 
 * @author anuj
 */
public class LanguageParms implements java.io.Serializable{
    private Map<String,String> langMap;
    private String blockStart;
    private String blockEnd;
    private String promptPre;
    private String promptSuf;

    public LanguageParms(){
    }

    public void setLangMap(Map<String,String> m){ langMap = m; }
    public void setBlockStart(String s){ blockStart = s; }
    public void setBlockEnd(String s){ blockEnd = s; }
    public void setPromptPre(String s){ promptPre = s; };
    public void setPromptSuf(String s){ promptSuf = s; };

    public Map<String,String> getLangMap(){ return langMap; }
    public String getBlockStart(){ return blockStart; }
    public String getBlockEnd(){ return blockEnd; }	
    public String getPromptPre(){ return promptPre; }
    public String getPromptSuf(){ return promptSuf; }

    public String toString(){
            return langMap.toString() + ":" + blockStart + ":" + blockEnd + ":" +
                            promptPre + ":" + promptSuf;
    }
}
