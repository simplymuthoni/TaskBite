import React, { useState } from 'react';
import { StyleSheet, View, Image, TextInput, Alert, ScrollView } from 'react-native';
import { Button, Text, Checkbox } from 'galio-framework';
import axios from 'axios';

export default function AuthScreen({ navigation }) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [repeatPassword, setRepeatPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [error, setError] = useState(null);

  const handleCreateAccount = async () => {
    // Reset error state
    setError(null);

    // Basic validation
    if (!name || !email || !password || !repeatPassword) {
      setError('All fields are required.');
      return;
    }

    if (password !== repeatPassword) {
      setError('Passwords do not match.');
      return;
    }

    try {
      const requestBody = {
        name,
        email,
        password,
      };

      const response = await axios.post(
        'http://127.0.0.1:8000/api/auth/register',
        requestBody,
      );

      if (response.data.success) {
        Alert.alert('Success', 'Account created successfully!');
        navigation.navigate('Login');
      } else {
        setError(response.data.error || 'Registration failed.');
      }
    } catch (error) {
      // Handle different error scenarios
      if (error.response && error.response.data && error.response.data.message) {
        setError(error.response.data.message);
      } else {
        setError('An unexpected error occurred. Please try again.');
      }
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Image source={require('../assets/logo.png')} style={styles.iconContainer} />
      
      <Text h1 style={styles.headerText}>
        Create Account
      </Text>

      <View style={styles.formContainer}>
        <Text size={16} color="#555" style={styles.subtitle}>
          Enter your details below
        </Text>

        <View style={styles.inputContainer}>
          <Text size={14} style={styles.label}>
            Name:
          </Text>
          <TextInput
            style={styles.input}
            value={name}
            onChangeText={setName}
            placeholder="John Doe"
            placeholderTextColor="#999"
          />
        </View>

        <View style={styles.inputContainer}>
          <Text size={14} style={styles.label}>
            Email:
          </Text>
          <TextInput
            style={styles.input}
            value={email}
            onChangeText={setEmail}
            placeholder="johndoe@example.com"
            keyboardType="email-address"
            autoCapitalize="none"
            placeholderTextColor="#999"
          />
        </View>

        <View style={styles.inputContainer}>
          <Text size={14} style={styles.label}>
            Password:
          </Text>
          <TextInput
            style={styles.input}
            value={password}
            onChangeText={setPassword}
            placeholder="********"
            secureTextEntry={true}
            placeholderTextColor="#999"
          />
        </View>

        <View style={styles.inputContainer}>
          <Text size={14} style={styles.label}>
            Repeat Password:
          </Text>
          <TextInput
            style={styles.input}
            value={repeatPassword}
            onChangeText={setRepeatPassword}
            placeholder="********"
            secureTextEntry={true}
            placeholderTextColor="#999"
          />
        </View>

        <Checkbox
          label="Remember me"
          checked={rememberMe}
          onChange={() => setRememberMe(!rememberMe)}
          style={styles.checkbox}
        />

        <Button
          round
          uppercase
          color="success"
          style={styles.button}
          onPress={handleCreateAccount}
        >
          Create Account
        </Button>

        <View style={styles.loginContainer}>
          <Text size={14} color="#555">
            Already have an account?
          </Text>
          <Button
            round
            uppercase
            color="info"
            style={styles.loginButton}
            onPress={() => navigation.navigate('Login')}
          >
            Login
          </Button>
        </View>

        {error && (
          <View style={styles.errorContainer}>
            <Text style={styles.errorText}>{error}</Text>
          </View>
        )}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    backgroundColor: '#f8f9fa',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  iconContainer: {
    width: 200,
    height: 150,
    resizeMode: 'contain',
    marginBottom: 20,
  },
  headerText: {
    marginBottom: 10,
    color: '#333',
  },
  subtitle: {
    marginBottom: 20,
    textAlign: 'center',
  },
  formContainer: {
    width: '100%',
    maxWidth: 400,
    padding: 20,
    backgroundColor: '#fff',
    borderRadius: 10,
    elevation: 3, // For Android shadow
    shadowColor: '#000', // For iOS shadow
    shadowOffset: { width: 0, height: 2 }, // For iOS shadow
    shadowOpacity: 0.25, // For iOS shadow
    shadowRadius: 3.84, // For iOS shadow
  },
  inputContainer: {
    marginBottom: 15,
  },
  label: {
    marginBottom: 5,
    color: '#333',
  },
  input: {
    height: 45,
    borderColor: '#ced4da',
    borderWidth: 1,
    borderRadius: 5,
    paddingHorizontal: 10,
    color: '#333',
    backgroundColor: '#fdfdfd',
  },
  checkbox: {
    marginVertical: 10,
  },
  button: {
    marginTop: 10,
    paddingVertical: 10,
  },
  loginContainer: {
    marginTop: 20,
    alignItems: 'center',
  },
  loginButton: {
    marginTop: 10,
    paddingVertical: 10,
    width: '60%',
  },
  errorContainer: {
    marginTop: 20,
    backgroundColor: '#f44336',
    padding: 10,
    borderRadius: 5,
  },
  errorText: {
    color: '#fff',
    fontSize: 14,
    textAlign: 'center',
  },
});
