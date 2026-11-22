import { router, Stack } from "expo-router";
import { PaperProvider } from "react-native-paper";
import { StyleSheet, Text, View } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { Button } from "react-native-paper";

export default function RootLayout() {
  const insets = useSafeAreaInsets();

  return (
    <PaperProvider>
      <Stack>
        <Stack.Screen name="(tabs)" options={{headerShown: true, headerTransparent: false, header: () => (
          <>
            <View style={{...stylesheet.header, paddingTop: insets.top + 5}}>
              <View>
                <Text>Hello, User</Text>
              </View>
              <View>
                <Button icon={"account"} mode="contained">Sign In</Button>
              </View>
            </View>
          </>
        )}}/>
      </Stack>
    </PaperProvider>
  );
}

const stylesheet = StyleSheet.create({
  header: {
    display: "flex",
    flexDirection: "row",
    justifyContent: "space-between",
    paddingLeft: 25,
    paddingRight: 25,
  },
});
