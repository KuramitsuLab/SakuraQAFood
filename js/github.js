/**
 * GitHub連携モジュール
 * ローカルファイルまたはGitHub APIからデータを取得
 */

const GitHubLoader = {
    /**
     * GitHubのURLをAPI URLに変換
     * @param {string} url - GitHub URL
     * @returns {string} API URL
     */
    convertToApiUrl(url) {
        // https://github.com/owner/repo/tree/branch/path/to/file
        // → https://api.github.com/repos/owner/repo/contents/path/to/file?ref=branch

        const githubPattern = /^https:\/\/github\.com\/([^\/]+)\/([^\/]+)\/(?:tree|blob)\/([^\/]+)\/(.+)$/;
        const match = url.match(githubPattern);

        if (!match) {
            throw new Error('無効なGitHub URLです');
        }

        const [, owner, repo, branch, path] = match;
        return `https://api.github.com/repos/${owner}/${repo}/contents/${path}?ref=${branch}`;
    },

    /**
     * ローカルファイルを取得
     * @param {string} path - ファイルパス
     * @returns {Promise<Object>} JSONデータ
     */
    async fetchLocal(path) {
        try {
            const response = await fetch(path);

            if (!response.ok) {
                throw new Error(`ファイルの読み込みに失敗しました (${response.status})`);
            }

            const data = await response.json();
            return data;
        } catch (error) {
            console.error('ローカルファイル取得エラー:', error);
            throw new Error(`ローカルファイルの読み込みに失敗しました: ${error.message}`);
        }
    },

    /**
     * GitHub APIからファイルを取得
     * @param {string} url - GitHub URL
     * @returns {Promise<Object>} JSONデータ
     */
    async fetchFromGitHub(url) {
        try {
            const apiUrl = this.convertToApiUrl(url);

            const response = await fetch(apiUrl, {
                headers: {
                    'Accept': 'application/vnd.github.v3+json'
                }
            });

            if (!response.ok) {
                if (response.status === 404) {
                    throw new Error('ファイルが見つかりませんでした');
                } else if (response.status === 403) {
                    throw new Error('アクセスが制限されています（レート制限またはプライベートリポジトリ）');
                }
                throw new Error(`GitHub APIエラー (${response.status})`);
            }

            const data = await response.json();

            // Base64デコード
            if (data.content) {
                const content = atob(data.content.replace(/\n/g, ''));
                return JSON.parse(content);
            } else {
                throw new Error('ファイルの内容が取得できませんでした');
            }
        } catch (error) {
            console.error('GitHub API取得エラー:', error);
            throw new Error(`GitHubからの読み込みに失敗しました: ${error.message}`);
        }
    },

    /**
     * データを取得（自動判定）
     * @param {string} pathOrUrl - ローカルパスまたはGitHub URL
     * @returns {Promise<Object>} JSONデータ
     */
    async fetch(pathOrUrl) {
        if (pathOrUrl.startsWith('https://github.com/')) {
            return this.fetchFromGitHub(pathOrUrl);
        } else {
            return this.fetchLocal(pathOrUrl);
        }
    }
};

// グローバルに公開
window.GitHubLoader = GitHubLoader;
