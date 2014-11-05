package com.as.iwebo.server.octave;

import java.io.*;
import java.util.Arrays;
import java.util.concurrent.ExecutionException;

/**
 * The class wraps Octave.
 * 
 * @author anuj
 */
public class OctaveEngine {
    /**
     * Octave initialization parameters (see octave documentation for parameter
     * descriptions).
     */
    private static final String[] CMD_ARRAY = {"octave", "--no-history",
        "--no-init-file", "--no-line-editing", "-i", "--no-site-file",
        "--silent"
    };
    /**
     * Handle to the running Octave process.
     */
    private final Process octaveProcess;
    /**
     * Handle to a writer to the stdin of Octave
     */
    private final OctaveInputWriter writer;
    /**
     * Handle to a reader of the stdout & stderr of Octave
     */
    private final OctaveOutputReader reader;
    
    public OctaveEngine() throws IOException{
        ProcessBuilder pb = new ProcessBuilder(Arrays.asList(CMD_ARRAY));
        //NOTE: This merges the stderr to stdout
        //I did this because I could not figure out the handling of these two
        //streams seperately without getting into a blocked state (:S) in some
        //cases. Future work involves fixing these and having the two streams 
        //seperately.
        pb.redirectErrorStream(true);
        octaveProcess = pb.start();
        reader = new OctaveOutputReader(
                new BufferedReader(new InputStreamReader(
                octaveProcess.getInputStream())));
        writer = new OctaveInputWriter( octaveProcess.getOutputStream() );
    }

    /**
     * Evaluates the command and returns Octave's response as a string.
     * 
     * @param cmd String command to be executed
     * @return String the response of octave to the execution
     * @throws java.lang.InterruptedException
     * @throws java.util.concurrent.ExecutionException
     * @throws java.io.IOException
     */
    public String evaluate(final String cmd) throws 
            InterruptedException, ExecutionException, IOException{
        final String s = writer.write(cmd);
        return reader.read(s);
    }    
    
}
