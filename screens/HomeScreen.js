import React from 'react';
import { StyleSheet, Text, View, Button, ImageBackground, Image } from 'react-native';

export default function HomeScreen({ navigation: { navigate } }) {
  return (
    <ImageBackground 
      source={require('../assets/s2.png')} 
      style={styles.backgroundImage}
    >
      <View style={styles.container}>
        <Image 
          source={require('../assets/logo.png')} 
          style={styles.logo} 
        />
        <Text style={styles.title}>Welcome to TaskBite</Text>
        <Text style={styles.subtitle}>
          Your one-stop solution for managing notes and to-do lists.
        </Text>

        <View style={styles.buttonContainer}>
          <Button title="Log in" onPress={() => navigate('Login')} color="#007BFF" />
          <View style={styles.space} />
          <Button
            title="Create account"
            onPress={() => navigate('Auth')}
            color="#28A745"
          />
        </View>
      </View>
    </ImageBackground>
  );
}

const styles = StyleSheet.create({
  backgroundImage: {
    flex: 1,
    resizeMode: 'cover',
    objectFit: 'fill'
  },
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
    backgroundColor: 'rgba(255, 255, 255, 0.7)', // Optional: adds a semi-transparent overlay
  },
  logo: {
    width: 100,
    height: 100,
    marginBottom: 30,
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
    justifyContent: 'center',
    alignItems: 'center',
  },
  space: {
    height: 20, // Adjust space between buttons as needed
  },
});
