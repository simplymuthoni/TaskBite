import React, { useState } from 'react';
import { StyleSheet, Text, View, TextInput, Alert, Image } from 'react-native';
import { Button, Checkbox } from 'galio-framework';

export default function LoginScreen({ navigation }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);

  const handleLogin = async () => {
    try {
      const response = await fetch('http://192.168.0.102:8000/api/auth/login', {
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
        // Store the token or user data if necessary, like in AsyncStorage or Redux
        Alert.alert('Login Successful', `Welcome ${data.user.name}`);
        
        // Redirect to the Dashboard screen
        navigation.navigate('Dashboard');
      } else {
        Alert.alert('Error', data.error);
      }
    } catch (error) {
      Alert.alert('Error', 'Failed to login');
    }
  };

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
      <Image source={require('../assets/logo.png')} style={styles.iconContainer} />
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
        <Checkbox
          label="Remember me"
          initialValue={rememberMe}
          onChange={(value) => setRememberMe(value)}
        />
      </View>

      <Button
        round
        color="info"
        onPress={handleLogin}
      >
        Login
      </Button>

      <View style={styles.forgotPasswordContainer}>
        <Button
          round
          color="warning"
          onPress={handleForgotPassword}
        >
          Forgot Password
        </Button>
      </View>

      <View style={styles.footer}>
        <Text>Don't have an account?</Text>
        <Button
          round
          color="success"
          onPress={() => navigation.navigate('Auth')}
        >
          Create Account
        </Button>
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
  iconContainer: {
    width: 300,
    height: 100,
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
    marginTop: 10,
    marginBottom: 20,
  },
  forgotPasswordContainer: {
    marginTop: 10,
    marginBottom: 20,
  },
  footer: {
    marginTop: 20,
    alignItems: 'center',
  },
});
