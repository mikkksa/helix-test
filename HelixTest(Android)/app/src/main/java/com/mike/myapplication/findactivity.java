package com.mike.myapplication;

import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Parcelable;
import android.view.View;
import android.widget.EditText;

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
import java.io.Serializable;
import java.io.StringReader;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

/**
 * Created by Mike on 31.12.2015.
 */
public class findactivity extends Activity {
    GlobalIP globalIP;
    EditText Group;
    ProgressDialog pd;

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.findactivity);
        globalIP = (GlobalIP)this.getApplication();
        String ip = globalIP.getIp();
        Group = (EditText) findViewById(R.id.editText);
    }

    public void find(View view) {
        ConnectTask connector = new ConnectTask();
        connector.globalIP = globalIP;
        connector.act = "getxml";
        connector.Group = String.valueOf(Group.getText());
        connector.activity = findactivity.this;
        connector.execute();

        pd = new ProgressDialog(this);
        pd.setTitle("Message");
        pd.setMessage("Collecting info");
        pd.show();
    }
}

class ConnectTask extends AsyncTask<Void, Void, List<Interview>>{
    public GlobalIP globalIP;
    public String act;
    public String Group;
    List<Interview> interviews_;
    public Activity activity;

    protected void onPostExecute(List<Interview> interviews1){
        globalIP.setInterviews(interviews_);
        Intent intent = new Intent(activity, ShowInterviewsActivity.class);
        activity.startActivity(intent);
    }

    @Override
    protected List<Interview> doInBackground(Void... params){
        if(act.equals("log"))
            Loggin();
        else if(act.equals("getxml")) {
            String xml = getxml(globalIP.getIp() + "/api/v1/interviews/?format=xml");
            try {
                interviews_ = get_ids_ints(xml);
                interviews_ = check_for_av(interviews_, globalIP.getIp() + "/andrints/");
            } catch (XmlPullParserException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        return interviews_;
    }

    public void Loggin(){
        HttpClient httpclient = new DefaultHttpClient();
        String curip = globalIP.getIp();
        HttpPost httppost = new HttpPost(curip + "/post/");
        try {
            List<NameValuePair> pairs = new ArrayList<NameValuePair>();
            pairs.add(new BasicNameValuePair("login", "s2"));
            pairs.add(new BasicNameValuePair("password", "1"));
            httppost.setEntity(new UrlEncodedFormEntity(pairs));

            HttpResponse response = httpclient.execute(httppost);
            HttpEntity entity = response.getEntity();
            String a = EntityUtils.toString(entity);
            //String b = EntityUtils.toString(entity);
        } catch (ClientProtocolException e) {
            // TODO Auto-generated catch block
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.getMessage();
        }
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

    public List<Interview> get_ids_ints(String xml) throws XmlPullParserException, IOException {
        List<Interview> interviews = new ArrayList<>();
        XmlPullParserFactory factory = XmlPullParserFactory.newInstance();
        factory.setNamespaceAware(true);
        XmlPullParser xpp = factory.newPullParser();
        xpp.setInput(new StringReader(xml));
        int eventType = xpp.getEventType();
        String xppname = "", name = "", group = "", id = "", userid = "";
        boolean visible = false;

        while(eventType != XmlPullParser.END_DOCUMENT) {
            if (eventType == XmlPullParser.START_DOCUMENT) {
                System.out.println("Start document");
            } else if (eventType == XmlPullParser.START_TAG) {
                System.out.println("Start tag " + xpp.getName());
                xppname = xpp.getName();
            } else if (eventType == XmlPullParser.END_TAG) {
                System.out.println("End tag " + xpp.getName());
            } else if (eventType == XmlPullParser.TEXT) {
                System.out.println("Text " + xpp.getText());
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
                        Interview interview;
                        interview = new Interview(visible, group, name, id, userid);
                        if (interview.group.equals(Group))
                            interviews.add(interview);
                        break;
                }
            }
            eventType = xpp.next();
        }
        System.out.println("End Document");
        return interviews;
    }

    public List<Interview> check_for_av(List<Interview> ints, String url){
        List<Interview> returnints = new ArrayList<>();
        HttpClient httpClient = new DefaultHttpClient();
        HttpPost httpPost = new HttpPost(url);
        String strints = "";
        for(int i =0; i < ints.size(); i++){
            if(i == ints.size() - 1)
                strints += ints.get(i).id;
            else
                strints += ints.get(i).id + "/";
        }

        try{
            List<NameValuePair> nameValuePairs = new ArrayList<>();
            nameValuePairs.add(new BasicNameValuePair("user", globalIP.getUserid()));
            nameValuePairs.add(new BasicNameValuePair("ints", strints));
            httpPost.setEntity(new UrlEncodedFormEntity(nameValuePairs));

            HttpResponse httpResponse = httpClient.execute(httpPost);
            HttpEntity httpEntity = httpResponse.getEntity();
            String[] strresponse = EntityUtils.toString(httpEntity).split("/");
            for(int i = 0; i < ints.size(); i++){
                boolean f = false;
                for (String aStrresponse : strresponse) {
                    if(aStrresponse.equals(ints.get(i).id))
                        f = true;
                }
                if(f)
                    returnints.add(ints.get(i));
            }
        } catch (ClientProtocolException e) {
            e.printStackTrace();
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        return returnints;
    }
}
