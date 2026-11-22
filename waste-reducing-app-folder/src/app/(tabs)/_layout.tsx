import { Tabs } from "expo-router";

export default function RootTabsLayout() {
  return (
    <Tabs>
      <Tabs.Screen
        name="index"
        options={{ title: "Home Page", headerShown: false }}
      />
    </Tabs>
  );
}
