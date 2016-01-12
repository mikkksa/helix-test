package com.mike.myapplication;

import android.app.Activity;
import android.content.Intent;
import android.os.AsyncTask;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.protocol.HTTP;
import org.w3c.dom.ls.LSException;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.List;
import java.util.jar.Attributes;


public class Choices_Activity extends Activity {
    Button next, end;
    String int_name, group;
    List<String> choices;
    EditText ch;
    public Toast toast;
    GlobalIP globalIP;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_choices_);
        next = (Button) findViewById(R.id.Next);
        end = (Button) findViewById(R.id.Next_end);
        int_name = getIntent().getStringExtra("Name");
        group = getIntent().getStringExtra("Group");
        choices = new ArrayList<>();
        ch = (EditText) findViewById(R.id.editText6);
        toast = Toast.makeText(getApplicationContext(), "Поле не должно быть пустым", Toast.LENGTH_SHORT);
        globalIP = (GlobalIP)this.getApplication();
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

    public void Next_Click(View v){
        if(!String.valueOf(ch.getText()).equals("")) {
            choices.add(String.valueOf(ch.getText()));
            ch.setText("");
        }
        else
            toast.show();
    }

    public void End_Click(View v){
        Next_Click(v);
        CreateTask create = new CreateTask();
        create.choices = choices;
        create.activity = Choices_Activity.this;
        create.execute(int_name, group, globalIP.getIp() + "/create_int_andr/", globalIP.getUserid());
    }
}


class CreateTask extends AsyncTask<String, Void, Void>{
    public List<String> choices;
    Choices_Activity activity;

    protected void onPostExecute(Void result){
        activity.startActivity(new Intent(activity, MainActivity.class));
    }

    @Override
    protected Void doInBackground(String... params) {
        String name_int = params[0];
        String group = params[1];
        String strchoices = "";
        String url = params[2];
        String user = params[3];

        for(int i =0; i < choices.size(); i++){
            if(i == choices.size() - 1)
                strchoices += choices.get(i);
            else strchoices += choices.get(i) + "/";
        }

        HttpClient client = new DefaultHttpClient();
        HttpPost post = new HttpPost(url);
        List<NameValuePair> pairs = new ArrayList<>();
        pairs.add(new BasicNameValuePair("int_name", name_int));
        pairs.add(new BasicNameValuePair("group", group));
        pairs.add(new BasicNameValuePair("choices", strchoices));
        pairs.add(new BasicNameValuePair("user_id", user));
        try {
            post.setEntity(new UrlEncodedFormEntity(pairs, HTTP.UTF_8));
            HttpResponse response = client.execute(post);
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