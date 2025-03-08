#include <bits/stdc++.h>
using namespace std;

// Function to write results to a file
void saveResults(string algo, int pageFaults) {
    ofstream fout("results.txt", ios::app); // Open file in append mode
    fout << algo << " " << pageFaults << endl;
    fout.close();
}

// Code for FIFO Page Replacement
void FIFO(vector<int> pages, int frames) {
    queue<int> frameQueue;
    unordered_map<int, bool> pageMap;
    int pageFaults = 0;
    
    for (int page : pages) {
        if (!pageMap[page]) { // If page fault occurs
            if (frameQueue.size() >= frames) { // Remove oldest page if full
                int oldest = frameQueue.front();
                frameQueue.pop();
                pageMap.erase(oldest);
            }
            frameQueue.push(page);
            pageMap[page] = true;
            pageFaults++;
        }
    }
    cout << "FIFO Page Faults: " << pageFaults << endl;
    saveResults("FIFO", pageFaults); // Save result for visualization
}

// Code to implement LRU Page Replacement
void LRU(vector<int> pages, int frames) {
    unordered_map<int, int> pageMap;
    int pageFaults = 0;

    for (int i = 0; i < pages.size(); i++) {
        if (pageMap.find(pages[i]) == pageMap.end()) { // Page fault
            if (pageMap.size() >= frames) {
                int lru = INT_MAX, pageToRemove;
                for (auto p : pageMap) {
                    if (p.second < lru) {
                        lru = p.second;
                        pageToRemove = p.first;
                    }
                }
                pageMap.erase(pageToRemove);
            }
            pageFaults++;
        }
        pageMap[pages[i]] = i; // Update last used index
    }
    cout << "LRU Page Faults: " << pageFaults << endl;
    saveResults("LRU", pageFaults);
}

// Code for Optimal Page Replacement
void Optimal(vector<int> pages, int frames) {
    vector<int> frame;
    int pageFaults = 0;

    for (int i = 0; i < pages.size(); i++) {
        auto it = find(frame.begin(), frame.end(), pages[i]);
        if (it == frame.end()) { // Page fault
            if (frame.size() >= frames) {
                int farthest = -1, pageToReplace;
                for (int j = 0; j < frame.size(); j++) {
                    int k;
                    for (k = i + 1; k < pages.size(); k++) {
                        if (pages[k] == frame[j]) break;
                    }
                    if (k == pages.size()) { // Page not used again
                        pageToReplace = j;
                        break;
                    }
                    if (k > farthest) {
                        farthest = k;
                        pageToReplace = j;
                    }
                }
                frame[pageToReplace] = pages[i];
            } else {
                frame.push_back(pages[i]);
            }
            pageFaults++;
        }
    }
    cout << "Optimal Page Faults: " << pageFaults << endl;
    saveResults("Optimal", pageFaults);
}

// The main function of cpp to run the above functions.
int main() {
    int frames, n;
    cout << "Enter the number of frames: ";
    cin >> frames;
    cout << "Enter the number of page references: ";
    cin >> n;

    vector<int> pages(n);
    cout << "Enter the page reference sequence: ";
    for (int i = 0; i < n; i++) {
        cin >> pages[i];
    }

    // Clear previous results
    ofstream fout("results.txt");
    fout.close();

    FIFO(pages, frames);
    LRU(pages, frames);
    Optimal(pages, frames);

    return 0;
}
