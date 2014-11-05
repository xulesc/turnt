package com.as.iwebo.server.octave;

import java.io.*;

/**
 * A class that provides a convinient wrapping of the input stream of octave.
 * 
 * @author anuj
 */
public class OctaveInputWriter {

    /**
     * Handle to the stdin of Octave.
     */
    private final OutputStream out;

    public OctaveInputWriter(final OutputStream out) {
        this.out = out;
    }
    
    /**
     * Writes the command along with a string to identify end of processing to
     * the input stream of octave.
     * 
     * @param cmd String the command to be executed
     * @return String the string to look for to determing end of execution on 
     * the output stream.
     * @throws java.io.IOException
     */
    public String write(final String cmd) throws IOException {
        String s = Math.random() + "BREAK: " + Math.random();
        out.write((cmd + "\r\n").getBytes());
        out.write(("printf(\"" + s + "\\n\")\r\n").getBytes());
        out.flush();
        return s;
    }
}
