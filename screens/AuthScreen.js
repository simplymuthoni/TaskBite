import React, { useState } from 'react';
import { StyleSheet, Text, View, Image, TextInput, CheckBox } from 'react-native';
import { Button } from 'galio-framework';

export default function AuthScreen({ navigation }) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [repeatPassword, setRepeatPassword] = useState('');

  const handleCreateAccount = () => {
    // TO DO: Implement create account logic here
    console.log('Create account button pressed');
  };

  const handleLogin = () => {
    // TO DO: Implement login logic here
    console.log('Login button pressed');
  };

  const handleForgotPassword = () => {
    // TO DO: Implement forgot password logic here
    console.log('Forgot password button pressed');
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
            onPress={() => navigation.navigate('Login')}
            >
            Login
          </Button>
        </View>
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
});