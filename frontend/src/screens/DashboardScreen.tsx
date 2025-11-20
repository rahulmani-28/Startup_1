import React from 'react';
import { View, Text, StyleSheet, Image } from 'react-native';

export function DashboardScreen() {
    return (
        <View style={styles.container}>
            <View style={styles.header}>
                <View style={styles.avatar} />
                <Text style={styles.name}>Demo User</Text>
                <Text style={styles.role}>Lorry Driver</Text>
            </View>

            <View style={styles.stats}>
                <View style={styles.statCard}>
                    <Text style={styles.statVal}>1,250</Text>
                    <Text style={styles.statLabel}>Total km</Text>
                </View>
                <View style={styles.statCard}>
                    <Text style={styles.statVal}>12</Text>
                    <Text style={styles.statLabel}>Journeys</Text>
                </View>
            </View>

            <Text style={styles.sectionTitle}>Recent Activity</Text>
            <View style={styles.activityItem}>
                <Text>Bangalore {'->'} Chennai</Text>
                <Text style={{ color: 'green' }}>Completed</Text>
            </View>
            <View style={styles.activityItem}>
                <Text>Mumbai {'->'} Pune</Text>
                <Text style={{ color: 'green' }}>Completed</Text>
            </View>
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, padding: 20 },
    header: { alignItems: 'center', marginBottom: 30 },
    avatar: { width: 80, height: 80, borderRadius: 40, backgroundColor: '#ddd', marginBottom: 10 },
    name: { fontSize: 24, fontWeight: 'bold' },
    role: { fontSize: 16, color: '#666' },
    stats: { flexDirection: 'row', justifyContent: 'space-around', marginBottom: 30 },
    statCard: { alignItems: 'center', backgroundColor: 'white', padding: 20, borderRadius: 10, width: '45%', elevation: 2 },
    statVal: { fontSize: 24, fontWeight: 'bold', color: '#2196f3' },
    statLabel: { color: '#666' },
    sectionTitle: { fontSize: 20, fontWeight: 'bold', marginBottom: 10 },
    activityItem: { flexDirection: 'row', justifyContent: 'space-between', padding: 15, backgroundColor: 'white', borderRadius: 5, marginBottom: 10 },
});
