import java.util.*;

import java.io.IOException;
import java.io.IOException;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.*;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapred.*;
import org.apache.hadoop.util.*;

public class CalculateMean {
    private static final String KEY = "M";

    // Mapper class
    public static class E_EMapper extends MapReduceBase implements Mapper<LongWritable, /* Input key Type */
            Text, /* Input value Type */
            Text, /* Output key Type */
            Text> /* Output value Type */
    {

        // Map function
        public void map(LongWritable key, Text value, OutputCollector<Text, Text> output, Reporter reporter)
                throws IOException {
            String line = value.toString();
            String out = line.split(",")[1] + ",1";
            output.collect(new Text(KEY), new Text(out));
        }
    }

    // Reducer class
    public static class E_EReduce extends MapReduceBase implements Reducer<Text, Text, Text, Text> {

        // Reduce function
        public void reduce(Text key, Iterator<Text> values, OutputCollector<Text, Text> output,
                Reporter reporter) throws IOException {
            double sum = .0;
            int count = 0;

            while (values.hasNext()) {
                String[] words = values.next().toString().split(",");
                sum += Double.parseDouble(words[0]);
                count += Integer.parseInt(words[1]);
            }

            String out = sum + "," + count;
            output.collect(new Text(KEY), new Text(out));

        }
    }

    // Main function
    public static void main(String args[]) throws Exception {
        JobConf conf = new JobConf(CalculateMean.class);

        conf.setJobName("calculate_mean");
        conf.setOutputKeyClass(Text.class);
        conf.setOutputValueClass(Text.class);
        conf.setMapperClass(E_EMapper.class);
        conf.setCombinerClass(E_EReduce.class);
        conf.setReducerClass(E_EReduce.class);
        conf.setInputFormat(TextInputFormat.class);
        conf.setOutputFormat(TextOutputFormat.class);

        FileInputFormat.setInputPaths(conf, new Path(args[0]));
        FileOutputFormat.setOutputPath(conf, new Path(args[1]));

        JobClient.runJob(conf);
    }
}
