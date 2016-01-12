package com.mike.myapplication;

import android.app.Activity;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;


public class ShowInterviewsActivity extends Activity {
    List<Interview> interviews;
    GlobalIP globalIP;
    List<String> names;
    ListView listView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_show_interviews);
        globalIP = (GlobalIP)this.getApplication();
        interviews = globalIP.getInterviews();
        names = new ArrayList<>();
        listView = (ListView) findViewById(R.id.listView);
        for(int i = 0;i<interviews.size();i++){
            names.add(interviews.get(i).name);
        }
        ArrayAdapter adapter = new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, names);
        listView.setAdapter(adapter);

        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {

            @Override
            public void onItemClick(AdapterView<?> parent, final View view,
                                    int position, long id) {
                final String item = (String) parent.getItemAtPosition(position);
                Interview interview = new Interview();
                for(int i = 0; i < interviews.size(); i++){
                    if(i == position)
                        interview = interviews.get(i);
                }
                TextView textView = (TextView) findViewById(R.id.textView2);
                textView.setText(interview.name);

                MyTask myTask = new MyTask();
                myTask.globalIP = globalIP;
                myTask.Interviewid = interview.id;
                myTask.activity = ShowInterviewsActivity.this;
                myTask.execute();
            }

        });
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_show_interviews, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            Intent intent = new Intent(ShowInterviewsActivity.this, SettingsActivity.class);
            startActivity(intent);
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
}


class MyTask extends AsyncTask<Void, Void, Void>{
    public GlobalIP globalIP;
    public String Interviewid;
    List<String> choices_id;
    Activity activity;

    protected void onPostExecute(Void result){
        Intent intent = new Intent(activity, DetailInterviewActivity.class);
        intent.putExtra("id", Interviewid);
        intent.putStringArrayListExtra("list", (ArrayList<String>)choices_id);
        activity.startActivity(intent);
    }

    @Override
    protected Void doInBackground(Void... params) {
        try {
            choices_id = get_choices_id();
            get_choices_names(choices_id);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    List<String> get_choices_id() throws IOException {
        List<String> result = new ArrayList<>();
        String url = globalIP.getIp() + "/getchid/";
        HttpClient httpClient = new DefaultHttpClient();
        HttpPost httpPost = new HttpPost(url);
        List<NameValuePair> pairs = new ArrayList<>();
        pairs.add(new BasicNameValuePair("id", Interviewid));
        httpPost.setEntity(new UrlEncodedFormEntity(pairs));

        HttpResponse httpResponse = httpClient.execute(httpPost);
        HttpEntity httpEntity = httpResponse.getEntity();
        String[] resultarray = EntityUtils.toString(httpEntity).split("/");
        Collections.addAll(result, resultarray);
        return result;
    }

    void get_choices_names(List<String> ids) throws IOException {
        String str_ids = "";
        for(int i =0; i <ids.size(); i++) {
            if (i == ids.size() - 1)
                str_ids += ids.get(i);
            else str_ids += ids.get(i) + "/";
        }

        List<String> result = new ArrayList<>();
        String url = globalIP.getIp() + "/getchnames/";
        HttpClient httpClient = new DefaultHttpClient();
        HttpPost httpPost = new HttpPost(url);
        List<NameValuePair> pairs = new ArrayList<>();
        pairs.add(new BasicNameValuePair("ids", str_ids));
        httpPost.setEntity(new UrlEncodedFormEntity(pairs));

        HttpResponse httpResponse = httpClient.execute(httpPost);
        HttpEntity httpEntity = httpResponse.getEntity();
        String[] resultarray = EntityUtils.toString(httpEntity).split("/");
        Collections.addAll(result, resultarray);
        List<Choice> choices = new ArrayList<>();

        for(int i = 0; i < result.size(); i++){
            Choice choice = new Choice(result.get(i), ids.get(i));
            choices.add(choice);
        }
        globalIP.setChoices(choices);
    }
}
