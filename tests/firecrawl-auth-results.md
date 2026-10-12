- **Firecrawl：成功。** 调用 `firecrawl_scrape` 抓取 `https://example.com`，返回 HTTP **200**，标题为 **Example Domain**；本次命中缓存。
- **Context7：成功。** 先调用 `resolve_library_id`，获得 `/vercel/next.js`，再调用 `query_docs` 查询 App Router。返回了 `app/` 文件路由、`page.tsx` 页面及 `layout.tsx` 根布局的文档与代码示例。

未使用 shell，未修改文件，未提交或推送，未暴露凭据。