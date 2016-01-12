package com.mike.myapplication;

import android.app.Activity;
import android.app.Application;
import android.app.ProgressDialog;
import android.content.Entity;
import android.content.Intent;
import android.os.AsyncTask;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;
import org.xmlpull.v1.XmlPullParser;
import org.xmlpull.v1.XmlPullParserException;
import org.xmlpull.v1.XmlPullParserFactory;

import java.io.IOException;
import java.io.StringReader;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.List;


public class MainActivity extends Activity {
    GlobalIP globalIP;
    ProgressDialog pd;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        globalIP = (GlobalIP)this.getApplication();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
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
    public void Search(View view)
    {
        Intent intent = new Intent(MainActivity.this, findactivity.class);
        startActivity(intent);
    }

    public void settings(View view){
        Intent intent = new Intent(MainActivity.this, SettingsActivity.class);
        startActivity(intent);
    }

    public void create_click(View v){
        startActivity(new Intent(MainActivity.this, CreateActivity.class));
    }

    public void look_results_click(View v){
        CheckedTask checkedTask = new CheckedTask();
        checkedTask.activity = MainActivity.this;
        checkedTask.globalIP = globalIP;
        checkedTask.execute(globalIP.getIp() + "/getcheckedids/");
        pd = new ProgressDialog(this);
        pd.setTitle("Message");
        pd.setMessage("Collecting info");
        pd.show();
    }
}

class CheckedTask extends AsyncTask<String, Void, Void>{
    public Activity activity;
    List<String> ids = new ArrayList<>();
    public GlobalIP globalIP;
    protected void onPostExecute(Void result){
        Intent intent = new Intent(activity, AvailableResultsActivity.class);
        activity.startActivity(intent);
    }

    @Override
    protected Void doInBackground(String... params) {
        String url = params[0];
        HttpClient client = new DefaultHttpClient();
        HttpPost post = new HttpPost(url);
        List<NameValuePair> pairs = new ArrayList<>();
        pairs.add(new BasicNameValuePair("user", globalIP.getUserid()));
        try {
            post.setEntity(new UrlEncodedFormEntity(pairs));
            HttpResponse response = client.execute(post);
            String[] ids_ = EntityUtils.toString(response.getEntity()).split("/");
            //Collections.addAll(ids, ids_);
            globalIP.setInterviews(getlist_ints(Arrays.asList(ids_), globalIP.getIp() + "/api/v1/interviews/?format=xml"));
        } catch (ClientProtocolException e) {
            e.printStackTrace();
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (XmlPullParserException e) {
            e.printStackTrace();
        }
        return null;
    }

    public List<Interview> getlist_ints(List<String> ids_, String url) throws XmlPullParserException, IOException {
        List<Interview> interviews = new ArrayList<>();
        String xml = getxml(url);
        XmlPullParserFactory factory = XmlPullParserFactory.newInstance();
        factory.setNamespaceAware(true);
        XmlPullParser xpp = factory.newPullParser();
        xpp.setInput(new StringReader(xml));
        int eventType = xpp.getEventType();
        String xppname = "", name = "", group = "", id = "", userid = "";
        boolean visible;

        while (eventType != XmlPullParser.END_DOCUMENT){
            if(eventType == XmlPullParser.START_TAG)
                xppname = xpp.getName();
            else if(eventType == XmlPullParser.TEXT){
                switch (xppname) {
                    case "group":
                        group = xpp.getText();
                        break;
                    case "name":
                        name = xpp.getText();
                        break;
                    case "id":
                        id = xpp.getText();
                        break;
                    case "user":
                        userid = xpp.getText();
                        break;
                    case "visible":
                        visible = xpp.getText().equals("True");
                        for(String id_: ids_){
                            if(id_.equals(id)) {
                                Interview interview;
                                interview = new Interview(visible, group, name, id, userid);
                                interviews.add(interview);
                            }
                        }
                        break;
                }
            }
            eventType = xpp.next();
        }
        return interviews;
    }

    public String getxml(String url){
        String xml = null;
        try{
            DefaultHttpClient httpClient = new DefaultHttpClient();
            HttpGet httpGet = new HttpGet(url);

            HttpResponse httpResponse = httpClient.execute(httpGet);
            HttpEntity httpEntity = httpResponse.getEntity();
            xml = EntityUtils.toString(httpEntity);
        } catch (ClientProtocolException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return xml;
    }
}


