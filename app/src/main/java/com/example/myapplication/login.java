package com.example.myapplication;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Patterns;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;

public class login extends AppCompatActivity {
    private EditText mEmail,mPass;
    private TextView mTextView;
    private Button mSignIn;
    CheckBox remember;
    private FirebaseAuth mAuth;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        mEmail = findViewById(R.id.username);
        mPass = findViewById(R.id.password);
        mTextView= findViewById(R.id.reg);
        mSignIn = findViewById(R.id.login);
        remember = findViewById(R.id.reme);

        mAuth = FirebaseAuth.getInstance();

        SharedPreferences logs = getSharedPreferences("checkbox",MODE_PRIVATE);
        String checkbox = logs.getString("remember","");
        if (checkbox.equals("true")){
            Intent intent = new Intent(login.this,MainActivity.class);
            startActivity(intent);
            finish();
        }
        else if (checkbox.equals("false")){
            Toast.makeText(this, "Please Sign In", Toast.LENGTH_SHORT).show();
        }

        mTextView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(login.this,registration.class));

            }
        });

        mSignIn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                loginUser();

            }
        });
        remember.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if (buttonView.isChecked()){
                    SharedPreferences logs = getSharedPreferences("checkbox",MODE_PRIVATE);
                    SharedPreferences.Editor editor = logs.edit();
                    editor.putString("remember","true");
                    editor.apply();

                }
                else if (!buttonView.isChecked()){
                    SharedPreferences logs = getSharedPreferences("checkbox",MODE_PRIVATE);
                    SharedPreferences.Editor editor = logs.edit();
                    editor.putString("remember","false");
                    editor.apply();

                }
            }
        });

    }

    private void loginUser() {
        String email = mEmail.getText().toString();
        String pass = mPass.getText().toString();

        if (!email.isEmpty() && Patterns.EMAIL_ADDRESS.matcher(email).matches()){
            if (!pass.isEmpty()){
                mAuth.signInWithEmailAndPassword(email,pass)
                        .addOnSuccessListener(new OnSuccessListener<AuthResult>() {
                            @Override
                            public void onSuccess(AuthResult authResult) {
                                if (mAuth.getCurrentUser().isEmailVerified()){
                                    Toast.makeText(login.this, "Login Successful", Toast.LENGTH_SHORT).show();
                                    startActivity(new Intent(login.this,MainActivity.class));
                                    finish();
                                }
                                else{
                                    Toast.makeText(login.this, "Please verify your email ID", Toast.LENGTH_SHORT).show();
                                }

                            }
                        }).addOnFailureListener(new OnFailureListener() {
                    @Override
                    public void onFailure(@NonNull Exception e) {
                        Toast.makeText(login.this, "Login Failed", Toast.LENGTH_SHORT).show();
                    }
                });


            }
            else{
                mPass.setError("Empty fields are not allowed");
            }
        }
        else if (email.isEmpty()){
            mEmail.setError("Empty fields are not allowed");
        }
        else{
            mEmail.setError("Enter a valid email address");
        }
    }

}