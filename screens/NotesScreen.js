import React from 'react';
import { StyleSheet, View, Text } from 'react-native';

export default function NotesScreen() {
  return (
    <View style={styles.container}>
      <Text>Notes Screen</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});
