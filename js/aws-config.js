/**
 * AWS設定ファイル
 *
 * 注意: このファイルには実際の認証情報が含まれるため、
 * .gitignoreに追加してGitにコミットしないでください。
 */

const AWS_CONFIG = {
    region: 'ap-northeast-1',
    bucketName: 'sakuraqa-food-review-results', // 実際のバケット名に置き換え
    apiEndpoint: 'https://ogllpkngp1.execute-api.ap-northeast-1.amazonaws.com/review', // 実際のAPI GatewayのURLに置き換え
    enableS3Upload: true
};

// グローバルスコープに公開
window.AWS_CONFIG = AWS_CONFIG;
