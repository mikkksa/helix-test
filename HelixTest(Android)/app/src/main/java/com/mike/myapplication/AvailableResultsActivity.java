package com.mike.myapplication;

import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Intent;
import android.os.AsyncTask;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;


public class AvailableResultsActivity extends Activity {
    GlobalIP globalIP;
    ListView listView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_available_results);
        List<String> names = new ArrayList<>();
        globalIP = (GlobalIP)this.getApplication();
        final List<Interview> interviews = globalIP.getInterviews();
        for(int i = 0; i < interviews.size(); i++){
            names.add(interviews.get(i).name);
        }
        listView=(ListView)findViewById(R.id.listView2);
        ArrayAdapter adapter = new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, names);
        listView.setAdapter(adapter);
        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                GetResultsTask task = new GetResultsTask();
                task.globalIP = globalIP;
                task.activity = AvailableResultsActivity.this;
                task.interview = interviews.get(position);
                task.execute(globalIP.getIp() + "/lookresint/");
            }
        });
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
}

class GetResultsTask extends AsyncTask<String, Void, Void>{
    public Interview interview;
    public Activity activity;
    public GlobalIP globalIP;

    protected void onPostExecute(Void result){
        Intent intent = new Intent(activity, ResultDetailActivity.class);
        activity.startActivity(intent);
    }

    @Override
    protected Void doInBackground(String... params) {
        HttpClient client = new DefaultHttpClient();
        HttpPost post = new HttpPost(params[0]);
        List<NameValuePair> pairs = new ArrayList<>();
        String result = "";
        List<String> res = new ArrayList<>();
        pairs.add(new BasicNameValuePair("interview", interview.id));
        try {
            post.setEntity(new UrlEncodedFormEntity(pairs));
            HttpResponse response = client.execute(post);
            HttpEntity entity = response.getEntity();
            result = EntityUtils.toString(entity);
        } catch (ClientProtocolException e) {
            e.printStackTrace();
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        res = Arrays.asList(result.split("/"));

        String choice = "";
        String pick = "";
        List<InterviewResult> results = new ArrayList<>();
        for(int i =0; i < res.size(); i++){
            if(i%2==0){
                choice = res.get(i);
            }
            else{
                pick = res.get(i);
                results.add(new InterviewResult(choice, pick));
            }
        }
        globalIP.setResults(results);
        return null;
    }
}