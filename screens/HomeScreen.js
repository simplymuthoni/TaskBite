import React from 'react';
import { StyleSheet, Text, View, Button } from 'react-native';

export default function HomeScreen({ navigation }) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome to TaskBite</Text>
      <Text style={styles.subtitle}>
        Your one-stop solution for managing notes and to-do lists.
      </Text>

      <View style={styles.buttonContainer}>
        <Button
          title="Login"
          onPress={() => navigation.navigate('Login')}
          color="#007BFF"
        />
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
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center',
    color: '#333',
  },
  subtitle: {
    fontSize: 18,
    textAlign: 'center',
    color: '#555',
    marginBottom: 40,
  },
  buttonContainer: {
    width: '80%',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
});
