import React from 'react';
import { StyleSheet, Text, View, Image } from 'react-native';
import { Button } from 'galio-framework';

/**
 * HomeScreen component that displays a welcome message and a button to navigate to the Auth screen.
 *
 * @param {object} props - Component props
 * @param {object} props.navigation - Navigation object
 * @returns {JSX.Element} HomeScreen component
 */
export default function HomeScreen({ navigation }) {
  return (
    <View style={styles.container}>
      <Image
        source={require('../assets/wallpaper1.png')} // Add background image
        style={styles.backgroundImage}
      />
      <View style={styles.overlayContainer}>
        <Image source={require('../assets/logo.png')} style={styles.iconContainer} />
        <Text h1>Welcome to <Text bold>TaskBite</Text></Text>
        <Button
          round
          uppercase
          color="success"
          onPress={() => navigation.navigate('Auth')}
        >
          Get Started
        </Button>
      </View>
    </View>
  );
}

/**
 * Styles for the HomeScreen component
 */
const styles = StyleSheet.create({
  /**
   * Container style
   */
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  /**
   * Background image style
   */
  backgroundImage: {
    flex: 1,
    resizeMode: 'cover',
    position: 'absolute',
    width: '100%',
    height: '100%',
    left: 0,
    right: 0,
    top: 0,
    bottom: 0,
  },
  /**
   * Overlay container style
   */
  overlayContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  /**
   * Icon container style
   */
  iconContainer: {
    width: 300,
    height: 200,
    marginBottom: 20,
  },
});