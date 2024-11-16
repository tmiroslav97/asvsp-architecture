package sales_country;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapred.*;

public class SalesCountryDriver {
    public static void main(String[] args) {
        JobClient myClient = new JobClient();
        // Create a configuration object for the job
        JobConf jobConf = new JobConf(SalesCountryDriver.class);

        // Set a name of the Job
        jobConf.setJobName("SalePerCountry");

        // Specify data type of output key and value
        jobConf.setOutputKeyClass(Text.class);
        jobConf.setOutputValueClass(IntWritable.class);

        // Specify names of Mapper and Reducer Class
        jobConf.setMapperClass(SalesMapper.class);
        jobConf.setReducerClass(SalesCountryReducer.class);

        // Specify formats of the data type of Input and output
        jobConf.setInputFormat(TextInputFormat.class);
        jobConf.setOutputFormat(TextOutputFormat.class);

        // Set input and output directories using command line arguments,
        // arg[0] = name of input directory on HDFS, and arg[1] = name of output
        // directory to be created to store the output file.

        FileInputFormat.setInputPaths(jobConf, new Path(args[0]));
        FileOutputFormat.setOutputPath(jobConf, new Path(args[1]));

        myClient.setConf(jobConf);
        try {
            // Run the job
            JobClient.runJob(jobConf);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
