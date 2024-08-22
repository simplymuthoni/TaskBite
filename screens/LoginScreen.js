import React, { useState } from 'react';
import { StyleSheet, Text, View, TextInput, Button, Alert, CheckBox } from 'react-native';

export default function LoginScreen({ navigation }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);

  /**
   * Handles the login button press
   *
   * @param {string} email - The email input value
   * @param {string} password - The password input value
   *
   * @example
   * handleLogin('johndoe@example.com', 'password123')
   */
  const handleLogin = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });

      const data = await response.json();
      if (data.success) {
        Alert.alert('Login Successful', `Email: ${email}`);
        // Store the token or user data in AsyncStorage or Redux
        // navigation.navigate('Home');
      } else {
        Alert.alert('Error', data.error);
      }
    } catch (error) {
      Alert.alert('Error', 'Failed to login');
    }
  };

  /**
   * Handles the forgot password button press
   *
   * @example
   * handleForgotPassword()
   */
  const handleForgotPassword = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/auth/forgot-password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
        }),
      });

      const data = await response.json();
      if (data.success) {
        Alert.alert('Forgot Password', 'Password reset email sent');
      } else {
        Alert.alert('Error', data.error);
      }
    } catch (error) {
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
        />
        <Text style={styles.label}>Remember me</Text>
      </View>

      <Button
        title="Login"
        onPress={handleLogin}
        color="#007BFF"
      />
      <b></b>

      <Button
        title="Forgot Password"
        onPress={handleForgotPassword}
        color="#DC3545"
        style={styles.forgotPasswordButton}
      />

      <View style={styles.footer}>
        <Text>Don't have an account?</Text>
        <Button
          title="Create Account"
          onPress={() => navigation.navigate('Auth')}
          color="#28A745"
        />
      </View>
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
    height:200,
    marginBottom: 15,
  },
  label: {
    marginBottom: 5,
    fontSize: 16,
  },
  input: {
    height: 30,
    borderColor: '#ced4da',
    borderWidth: 1,
    padding: 10,
    backgroundColor: '#fff',
  },
  inputContainer: {
    marginBottom: 20,
  },
  formContainer: {
    padding: 20,
  },
  rememberMeContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 10,
    marginBottom: 20,
  },
  forgotPasswordButton: {
    marginTop: 10,
    marginBottom: 20,
    padding:20,
  },
  loginButton:{
    padding: 20,
    marginTop: 10,
    marginBottom:20,
  },
  footer: {
    marginTop: 20,
    alignItems: 'center',
  },
});
