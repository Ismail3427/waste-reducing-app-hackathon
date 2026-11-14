import { Text, View, StyleSheet, ScrollView } from "react-native";

export default function Index() {
  return (
    <ScrollView contentContainerStyle={styles.mainContainer}>
      <View>
        <Text>Welcome to our app</Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  mainContainer: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
  },
});
