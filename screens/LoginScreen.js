import React, { useState } from 'react';
import { StyleSheet, Text, View, TextInput, Button, Alert, CheckBox } from 'react-native';

export default function LoginScreen({ navigation }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);

  const handleLogin = () => {
    // TODO: Implement login logic here
    // For now, just show an alert
    if (email && password) {
      Alert.alert('Login Successful', `Email: ${email}`);
    } else {
      Alert.alert('Error', 'Please enter both email and password');
    }
  };

  const handleForgotPassword = () => {
    // Implement forgot password logic here
    Alert.alert('Forgot Password', 'Forgot password functionality not implemented yet');
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

      <Button
        title="Login"
        onPress={handleLogin}
        color="#007BFF"
      />
      <View style={styles.rememberMeContainer}>
          <CheckBox
            value={rememberMe}
            onValueChange={(value) => setRememberMe(value)}
          />
          <Text>Remember me</Text>
        </View>

        <Button
          title="Forgot Password"
          onPress={handleForgotPassword}
          color="danger"
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
  formContainer:{
    padding:20,
  },
  headerText: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  inputContainer: {
    width: '100%',
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
    paddingHorizontal: 10,
    borderRadius: 5,
    backgroundColor: '#fff',
  },
  footer: {
    marginTop: 20,
    alignItems: 'center',
  },
  rememberMeContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 10,
  },
});