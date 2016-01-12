package com.mike.myapplication;

import android.app.Activity;
import android.content.Intent;
import android.os.AsyncTask;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Adapter;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;

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
import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.List;


public class DetailInterviewActivity extends Activity {
    Interview interview;
    GlobalIP globalIP;
    TextView textView;
    List<String> ids;
    ListView listView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_detail_interview);
        textView = (TextView) findViewById(R.id.int_name);
        String id = getIntent().getStringExtra("id");
        ids = getIntent().getStringArrayListExtra("list");
        globalIP = (GlobalIP)this.getApplication();
        for(int i = 0; i < globalIP.getInterviews().size(); i++){
            if(globalIP.getInterviews().get(i).id.equals(id))
                interview = globalIP.getInterviews().get(i);
        }
        textView.setText(interview.name);

        List<String> names = new ArrayList<>();
        for(Choice c:globalIP.getChoices()){
            names.add(c.name);
        }
        listView = (ListView) findViewById(R.id.choices);
        ArrayAdapter adapter = new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, names);
        listView.setAdapter(adapter);

        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                String item = (String) parent.getItemAtPosition(position);
                String id_ = "";
                for(int i = 0; i < globalIP.getChoices().size();i++){
                    if(globalIP.getChoices().get(i).name.equals(item))
                        id_ = globalIP.getChoices().get(i).id;
                }
                //String item = ids.get(position);
                Sender sender = new Sender();
                sender.id = id_;
                sender.activity = DetailInterviewActivity.this;
                sender.execute(globalIP);

            }
        });
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_detail_interview, menu);
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
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
}


class Sender extends AsyncTask<GlobalIP, Void, Void>{
    public String id;
    public Activity activity;

    protected void onPostExecute(Void result){
        activity.startActivity(new Intent(activity, MainActivity.class));
    }

    @Override
    protected Void doInBackground(GlobalIP... globalIPs) {

        HttpClient httpClient = new DefaultHttpClient();
        HttpPost httpPost = new HttpPost(globalIPs[0].getIp() + "/send_int_res/");
        List<NameValuePair> pairs = new ArrayList<>();
        pairs.add(new BasicNameValuePair("user", globalIPs[0].getUserid()));
        pairs.add(new BasicNameValuePair("id", id));
        try {
            httpPost.setEntity(new UrlEncodedFormEntity(pairs));
            HttpResponse response = httpClient.execute(httpPost);
        } catch (ClientProtocolException e) {
            e.printStackTrace();
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        return null;
    }
}