package com.mike.myapplication;

import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.Entity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.inputmethod.InputMethodManager;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

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
import java.util.List;


public class LoginActivity extends Activity {
    EditText login;
    EditText pass;
    GlobalIP globalIP;
    public Toast toast;
    public ProgressDialog pd;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        login = (EditText) findViewById(R.id.editText2);
        pass = (EditText) findViewById(R.id.editText3);
        globalIP = (GlobalIP)this.getApplication();
        toast = Toast.makeText(getApplicationContext(), "Неверный логин или пароль", Toast.LENGTH_SHORT);
        SharedPreferences settings = getPreferences(0);
        String login_ = settings.getString("Login", "");
        String pass_ = settings.getString("Pass", "");
        login.setText(login_);
        pass.setText(pass_);
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

    public void login(View view){
        SharedPreferences settings = getPreferences(0);
        SharedPreferences.Editor editor = settings.edit();
        editor.putString("Login", String.valueOf(login.getText()));
        editor.putString("Pass", String.valueOf(pass.getText()));

        editor.apply();
        LoginTask loginTask = new LoginTask();
        loginTask.globalIP = globalIP;
        loginTask.activity = LoginActivity.this;
        loginTask.execute(globalIP.getIp() + "/get_user_id/", String.valueOf(login.getText()),
                String.valueOf(pass.getText()));

        pd = new ProgressDialog(this);
        pd.setTitle("Message");
        pd.setMessage("Logging in...");
        pd.show();
    }

    public void settings_(View v){
        startActivity(new Intent(LoginActivity.this, SettingsActivity.class));
    }
}


class LoginTask extends AsyncTask<String, Void, Void>{
    GlobalIP globalIP;
    LoginActivity activity;

    @Override
    protected Void doInBackground(String... params) {
        String url = params[0];
        String login = params[1];
        String pass = params[2];
        String result = "";

        HttpClient httpClient = new DefaultHttpClient();
        HttpPost post = new HttpPost(url);
        List<NameValuePair> pairs = new ArrayList<>();
        pairs.add(new BasicNameValuePair("login", login));
        pairs.add(new BasicNameValuePair("password", pass));
        try {
            post.setEntity(new UrlEncodedFormEntity(pairs));
            HttpResponse response = httpClient.execute(post);
            HttpEntity entity = response.getEntity();
            result = EntityUtils.toString(entity);
            globalIP.setUserid(result);
        } catch (ClientProtocolException e) {
            e.printStackTrace();
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        activity.pd.dismiss();
        if(!result.equals("") && !result.equals("None"))
            activity.startActivity(new Intent(activity, MainActivity.class));
        else{
            activity.toast.show();
        }
        return null;
    }
}