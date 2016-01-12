package com.mike.myapplication;

import android.app.Activity;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.Adapter;
import android.widget.ArrayAdapter;
import android.widget.ListView;

import java.util.ArrayList;
import java.util.List;


public class ResultDetailActivity extends Activity {
    ListView listView;
    GlobalIP globalIP;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_result_detail);
        listView = (ListView)findViewById(R.id.listView3);
        globalIP = (GlobalIP)this.getApplication();
        List<InterviewResult> results = globalIP.getResults();
        List<String> names = new ArrayList<>();
        int allchoices = 0;

        for(int i =0; i < results.size(); i++){
            allchoices += Integer.parseInt(results.get(i).pick);
        }

        for(int i = 0; i < results.size(); i++){
            Double piece = (double)Integer.parseInt(results.get(i).pick)*100/allchoices;
            piece *= 1000;
            int d = (int)Math.round(piece);
            piece = (double)d/1000;
            names.add(results.get(i).choice + "\t" + String.valueOf(piece) + "%");
        }
        ArrayAdapter adapter = new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, names);
        listView.setAdapter(adapter);
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
