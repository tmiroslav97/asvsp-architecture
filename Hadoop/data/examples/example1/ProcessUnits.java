import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;

public class ProcessUnits {
    public static class UnitsMapper extends Mapper<LongWritable, Text, Text, IntWritable> {
        @Override
        public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
            StringTokenizer tokens = new StringTokenizer(value.toString());
            if (!tokens.hasMoreTokens()) return;
            String year = tokens.nextToken();
            String lastToken = null;
            while (tokens.hasMoreTokens()) lastToken = tokens.nextToken();
            if (lastToken == null) return;
            try {
                context.write(new Text(year), new IntWritable(Integer.parseInt(lastToken)));
            } catch (NumberFormatException ignored) {
                // Ignore malformed input records.
            }
        }
    }

    public static class AboveThresholdReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
        private static final int THRESHOLD = 30;

        @Override
        public void reduce(Text key, Iterable<IntWritable> values, Context context)
                throws IOException, InterruptedException {
            for (IntWritable value : values) {
                if (value.get() > THRESHOLD) context.write(key, value);
            }
        }
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 2) {
            System.err.println("Usage: ProcessUnits <input> <output>");
            System.exit(2);
        }
        Job job = Job.getInstance(new Configuration(), "max_electricity_units");
        job.setJarByClass(ProcessUnits.class);
        job.setMapperClass(UnitsMapper.class);
        job.setReducerClass(AboveThresholdReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);
        job.setInputFormatClass(TextInputFormat.class);
        job.setOutputFormatClass(TextOutputFormat.class);
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
