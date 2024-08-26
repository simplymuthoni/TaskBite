import React, { useState } from 'react';
import { StyleSheet, Text, View, Image, TextInput} from 'react-native';
import { Button } from 'galio-framework';
import axios from 'axios';

export default function AuthScreen({ navigation }) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [repeatPassword, setRepeatPassword] = useState('');
  const [error, setError] = useState(null);

  const handleCreateAccount = async () => {
    try {
      const response = await axios.post('https://127.0.0.1:8000/api/auth/register', {
        name,
        email,
        password,
      });
      console.log(response.data);
      navigation.navigate('Login');
    } catch (error) {
      setError(error.response.data.message);
    }
  };

  const handleLogin = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/auth/login', {
        email,
        password,
      });
      console.log(response.data);
      navigation.navigate('Home');
    } catch (error) {
      setError(error.response.data.message);
    }
  };

  const handleForgotPassword = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/auth/forgot-password', {
        email,
      });
      console.log(response.data);
    } catch (error) {
      setError(error.response.data.message);
    }
  };
  
  return (
    <View style={styles.container}>
      <Image source={require('../assets/logo.png')} style={styles.iconContainer} />
      <Text h1>Create Account / Login</Text>
      <b></b>

      <View style={styles.formContainer}>
        <Text>Enter your details below</Text>

        <View style={styles.inputContainer}>
          <Text>Name:</Text>
          <TextInput
            style={styles.input}
            value={name}
            onChangeText={(text) => setName(text)}
            placeholder="John Doe"
          />
        </View>

        <View style={styles.inputContainer}>
          <Text>Email:</Text>
          <TextInput
            style={styles.input}
            value={email}
            onChangeText={(text) => setEmail(text)}
            placeholder="johndoe@example.com"
          />
        </View>

        <View style={styles.inputContainer}>
          <Text>Password:</Text>
          <TextInput
            style={styles.input}
            value={password}
            onChangeText={(text) => setPassword(text)}
            placeholder="********"
            secureTextEntry={true}
          />
        </View>

        <View style={styles.inputContainer}>
          <Text>Repeat Password:</Text>
          <TextInput
            style={styles.input}
            value={repeatPassword}
            onChangeText={(text) => setRepeatPassword(text)}
            placeholder="********"
            secureTextEntry={true}
          />
        </View>

        <Button
          round
          uppercase
          color="success"
          onPress={handleCreateAccount}
        >
          Create Account
        </Button>

        <View style={styles.loginContainer}>
          <Text>Already have an account?</Text>
          <Button
            round
            uppercase
            color="info"
            onPress={handleLogin}
            >
            Login
          </Button>
        </View>

        <View style={styles.forgotPasswordContainer}>
          <Text>Forgot Password?</Text>
          <Button
            round
            uppercase
            color="warning"
            onPress={handleForgotPassword}
            >
            Forgot Password
          </Button>
        </View>

        {error && (
          <View style={styles.errorContainer}>
            <Text style={styles.errorText}>{error}</Text>
          </View>
        )}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  iconContainer: {
    width: 300,
    height: 200,
    marginBottom: 20,
  },
  formContainer: {
    padding: 20,
  },
  inputContainer: {
    marginBottom: 20,
  },
  input: {
    height: 30,
    borderColor: '#ccc',
    borderWidth: 1,
    padding: 10,
  },
  loginContainer: {
    marginTop: 20,
  },
  forgotPasswordContainer: {
    marginTop: 20,
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