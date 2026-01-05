/**
 * Butterfly Frontend - Global State Store
 * 
 * Using Zustand for simple state management.
 */
import { create } from 'zustand';
import { Dataset, Experiment, Run } from '../api/client';

interface ButterflyStore {
    // Data
    datasets: Dataset[];
    experiments: Experiment[];
    currentExperiment: Experiment | null;
    currentRun: Run | null;

    // Actions
    setDatasets: (datasets: Dataset[]) => void;
    setExperiments: (experiments: Experiment[]) => void;
    setCurrentExperiment: (experiment: Experiment | null) => void;
    setCurrentRun: (run: Run | null) => void;
}

export const useStore = create<ButterflyStore>((set) => ({
    datasets: [],
    experiments: [],
    currentExperiment: null,
    currentRun: null,

    setDatasets: (datasets) => set({ datasets }),
    setExperiments: (experiments) => set({ experiments }),
    setCurrentExperiment: (experiment) => set({ currentExperiment: experiment }),
    setCurrentRun: (run) => set({ currentRun: run }),
}));
