import React, { useState } from 'react';
import { StyleSheet, Text, View, TextInput, Alert } from 'react-native';
import axios from 'axios';
import { Button, CheckBox } from 'galio-framework';

export default function LoginScreen({ navigation }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [error, setError] = useState(null);

  /**
   * Handles the login button press
   */
  const handleLogin = async () => {
    try {
      const response = await axios.post(
        'http://127.0.0.1:8000/api/auth/login',
        { email, password }
      );

      const { success, error } = response.data;
      if (success) {
        Alert.alert('Login Successful', `Email: ${email}`);
        // Store the token or user data in AsyncStorage or Redux
        // navigation.navigate('Home');
      } else {
        setError(error);
        Alert.alert('Error', error);
      }
    } catch (error) {
      setError('Failed to login');
      Alert.alert('Error', 'Failed to login');
    }
  };

  /**
   * Handles the forgot password button press
   */
  const handleForgotPassword = async () => {
    try {
      const requestBody = JSON.stringify({ email });
      const response = await fetch('http://127.0.0.1:8000/api/auth/forgot-password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: requestBody,
      });

      const responseData = await response.json();
      const { success, error } = responseData;

      if (success) {
        Alert.alert('Forgot Password', 'Password reset email sent');
      } else {
        setError(error);
        Alert.alert('Error', error);
      }
    } catch (error) {
      setError('Failed to send password reset email');
      Alert.alert('Error', 'Failed to send password reset email');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.headerText}>Login</Text>

      <View style={styles.inputContainer}>
        <Text style={styles.label}>Email:</Text>
        <TextInput
          style={styles.input}
          value={email}
          onChangeText={(text) => setEmail(text)}
          placeholder="johndoe@example.com"
          keyboardType="email-address"
        />
      </View>

      <View style={styles.inputContainer}>
        <Text style={styles.label}>Password:</Text>
        <TextInput
          style={styles.input}
          value={password}
          onChangeText={(text) => setPassword(text)}
          placeholder="********"
          secureTextEntry={true}
        />
      </View>

      <View style={styles.rememberMeContainer}>
        <CheckBox
          value={rememberMe}
          onValueChange={(value) => setRememberMe(value)}
          label="Remember me"
        />
      </View>

      <Button
        round
        uppercase
        style={styles.loginButton}
        color="#007BFF"
        onPress={handleLogin}
      >
        Login
      </Button>

      <Button
        round
        color="#DC3545"
        style={styles.forgotPasswordButton}
        onPress={handleForgotPassword}
      >
        Forgot Password
      </Button>

      <View style={styles.footer}>
        <Text>Don't have an account?</Text>
        <Button
          round
          color="#28A745"
          onPress={() => navigation.navigate('Auth')}
        >
          Create Account
        </Button>
      </View>

      {error && (
        <View style={styles.errorContainer}>
          <Text style={styles.errorText}>{error}</Text>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
    backgroundColor: '#f8f9fa',
  },
  headerText: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  inputContainer: {
    width: 300,
    marginBottom: 15,
  },
  label: {
    marginBottom: 5,
    fontSize: 16,
  },
  input: {
    height: 40,
    borderColor: '#ced4da',
    borderWidth: 1,
    padding: 10,
    backgroundColor: '#fff',
  },
  rememberMeContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 20,
  },
  forgotPasswordButton: {
    marginBottom: 20,
  },
  loginButton: {
    marginBottom: 20,
  },
  footer: {
    marginTop: 20,
    alignItems: 'center',
  },
  errorContainer: {
    marginTop: 20,
    backgroundColor: '#f44336',
    padding: 10,
    borderRadius: 5,
  },
  errorText: {
    color: '#fff',
    fontSize: 16,
  },
});
