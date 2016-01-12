package com.mike.myapplication;

import android.app.Activity;
import android.content.Intent;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.EditText;


public class CreateActivity extends Activity {
    EditText name, group;
    String Name, Group;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_create);
        name = (EditText) findViewById(R.id.editText4);
        group = (EditText) findViewById(R.id.editText5);
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

    public void Choices_Click(View v){
        Name = String.valueOf(name.getText());
        Group = String.valueOf(group.getText());
        Intent intent = new Intent(CreateActivity.this, Choices_Activity.class);
        intent.putExtra("Name", Name);
        intent.putExtra("Group", Group);
        startActivity(intent);
    }
}
