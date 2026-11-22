import { StyleSheet, Text, View } from "react-native";
import { TextInput } from "react-native-paper";

const LoginComponent = () => {
  return (
    <View style={styles.main}>
      <View>
        <Text>Email Address</Text>
        <TextInput
          placeholder="user@example.com"
          keyboardType="email-address"
        />
      </View>
      <View>
        <Text>Password</Text>
        <TextInput
          placeholder="SuperSecurePassword1234!"
          keyboardType="visible-password"
        />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  main: {
    display: "flex",
    flexDirection: "column",
    gap: 15,
    padding: 15
  },
});

export default LoginComponent;
