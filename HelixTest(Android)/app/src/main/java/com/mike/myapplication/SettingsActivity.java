package com.mike.myapplication;

import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;

/**
 * Created by ������ on 04.01.2016.
 */
public class SettingsActivity extends Activity{
    TextView curip;
    GlobalIP globalIP;
    EditText edip;
    @Override
    protected void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        setContentView(R.layout.settingsactivity);
        curip  = (TextView)findViewById(R.id.curiptext);
        edip = (EditText) findViewById(R.id.changetext);
        globalIP=(GlobalIP)this.getApplication();
        String ip = globalIP.getIp();
        curip.append(ip);
    }

    public void changeip(View view){
        String newip = "http://" + edip.getText();
        globalIP.setip(newip);
        curip.setText("Текущий IP: " + globalIP.getIp());
    }

    public void exit_click(View v){
        SharedPreferences settings = getPreferences(0);
        SharedPreferences.Editor editor = settings.edit();
        editor.putString("Login", "");
        editor.putString("Pass", "");

        editor.apply();
        startActivity(new Intent(SettingsActivity.this, LoginActivity.class));
    }
}
