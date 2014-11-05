package com.as.iwebo.server.octave;

import java.io.*;
import java.util.concurrent.*;

/**
 * A class that provides a convinient wrapping for the output stream of Octave.
 * Assumes that the stderr stream has been merged with the stdout stream. 
 * 
 * This class will change in the future to handle the stdout and stderr stream
 * seperately.
 * 
 * @author anuj
 */
public class OctaveOutputReader {
    /**
     * Handle to the output stream of Octave
     */
    private final BufferedReader in;
    /**
     * Time in milliseconds for which the reader sleeps while waiting for output
     * to appear on the Octave stdout.
     */
    private final int sleepTime = 100;
    private final ExecutorService exec = Executors.newSingleThreadExecutor();

    public OctaveOutputReader(final BufferedReader in) {
        this.in = in;
    }

    public String read(final String spacer) throws
            InterruptedException, ExecutionException {
        return exec.submit(new OutputCallable(spacer)).get();
    }

    public void close() {
        exec.shutdownNow();
    }
    
    /**
     * The class is instantiated for every command that is submitted to the
     * Octave process. It waits for the reponse to appear on the stdout and
     * collects the output till the spacer is encountered when it terminates.
     */
    class OutputCallable implements Callable<String> {
        private final String spacer;
        
        public OutputCallable(final String s) {
            spacer = s;
        }

        public String call() throws IOException, InterruptedException {
            String ret = "", b;
            while (!in.ready()) {
                TimeUnit.MILLISECONDS.sleep(sleepTime);
            }
            while ((b = in.readLine()) != null) {
                if (b.contains(spacer)) {
                    break;
                }
                ret += b.replaceAll("(octave:\\d>)", "").trim() + "\n";
            }
            return ret;
        }
    }
}
