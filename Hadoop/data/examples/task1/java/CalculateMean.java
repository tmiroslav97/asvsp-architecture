import java.io.IOException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class CalculateMean {
    private static final Text KEY = new Text("M");

    public static class MeanMapper extends Mapper<LongWritable, Text, Text, DoubleWritable> {
        @Override
        public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
            String[] columns = value.toString().split(",");
            if (columns.length < 2) return;
            try {
                context.write(KEY, new DoubleWritable(Double.parseDouble(columns[1])));
            } catch (NumberFormatException ignored) {
                // Ignore headers and malformed records.
            }
        }
    }

    public static class MeanReducer extends Reducer<Text, DoubleWritable, Text, Text> {
        @Override
        public void reduce(Text key, Iterable<DoubleWritable> values, Context context)
                throws IOException, InterruptedException {
            double sum = 0.0;
            long count = 0;
            for (DoubleWritable value : values) {
                sum += value.get();
                count++;
            }
            if (count > 0) context.write(key, new Text(sum + "," + count));
        }
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 2) {
            System.err.println("Usage: CalculateMean <input> <output>");
            System.exit(2);
        }
        Job job = Job.getInstance(new Configuration(), "calculate_mean");
        job.setJarByClass(CalculateMean.class);
        job.setMapperClass(MeanMapper.class);
        job.setReducerClass(MeanReducer.class);
        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(DoubleWritable.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
