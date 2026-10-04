# CRM 원본·리뉴얼 화면 대응

42개 CRM 화면과 로그인은 읽기 전용으로 확인했습니다. 마이그레이션은 원본 미열람 제안입니다. 44개 화면을 Pretendard와 공통 뉴트럴 Bento 테마로 통일했습니다.

| 화면 | 원본 경로 | 시안 | 개선 방향 |
| --- | --- | --- | --- |
| 대시보드 | /pages/member/dashboard/index.php | [보기](https://leejinho970715-star.github.io/CRM/#home) | 할 일·리드·계약·갱신을 요약하고 후속 업무로 연결. 겹친 입체 카드와 짧은 그림자를 절제해 사용하며, 본문 너비에 맞춰 요약 카드·폼·차트를 재배치 |
| 고객사 관리 | /pages/member/customer/company_list.php | [보기](https://leejinho970715-star.github.io/CRM/#customers) | 기본·상세 조건 유지, 핵심 열 우선, 상세 패널에 고객 정보·이력·수정·활동 기록 묶기 |
| 비영리 관리 | /pages/member/customer/nonprofit_management.php | [보기](https://leejinho970715-star.github.io/CRM/#nonprofits) | 설립 단계·예산 편성 시기·알림 주기를 별도 입력 묶음으로 유지 |
| 영리·비영리 뉴스 | /pages/member/customer/nonprofit_news.php | [보기](https://leejinho970715-star.github.io/CRM/#news) | 연계 고객과 기회 유형, 관심 기사와 후속 업무를 함께 배치 |
| 컨택 관리 | /pages/member/contact/contact_main.php | [보기](https://leejinho970715-star.github.io/CRM/#contacts) | 넓은 행 내 편집을 상세 패널로 옮기고 소속·연락·이직·퇴사·메일 후속관리 연결 |
| 고객사 일괄업로드 | /pages/member/customer/company_excel_upload.php | [보기](https://leejinho970715-star.github.io/CRM/#upload) | 파일→항목→검증→결과 4단계로 정리하고 오류 행을 반영 전 확인 |
| 영업활동 관리 | /pages/member/activity/activity_register.php | [보기](https://leejinho970715-star.github.io/CRM/#activity) | 고객 선택→기본 정보→내용→처리 결과·다음 행동을 연결; 실제 유형/처리 결과/제품 선택지 보완 |
| 오늘의 업무함 | /pages/member/sales/task_board.php | [보기](https://leejinho970715-star.github.io/CRM/#tasks) | 기한 경과·오늘·예정·완료와 목록·보드·달력 전환, 필요한 때 등록 폼 열기 |
| 통합 리드함 | /pages/member/sales/lead_inbox.php | [보기](https://leejinho970715-star.github.io/CRM/#leads) | 문의·배정·우선순위·응답기한을 비교하고 첫 연락 업무 생성 |
| 견적 현황 | /pages/member/activity/quote_status.php | [보기](https://leejinho970715-star.github.io/CRM/#quotes) | 금액·제품·상태 요약과 상세 상담/첨부를 연결 |
| 마케팅 활동 | /pages/member/marketing/marketing_activity_register.php | [보기](https://leejinho970715-star.github.io/CRM/#marketing) | 기존/신규 대상, 활동 정보, 내용·리드 단계/점수로 입력 묶기 |
| 연간 영업현황 | /pages/member/activity/activity_year.php?year=2026 | [보기](https://leejinho970715-star.github.io/CRM/#yearly) | 기간·담당자·유형 조건, 집계 요약, 추이 그래프와 원본 목록을 같은 기준으로 표시 |
| 활동별 업체별 현황 | /pages/member/activity/activity_detail_status.php | [보기](https://leejinho970715-star.github.io/CRM/#activity-detail) | 활동 유형·거래처·상태 필터로 좁히고 상세 상담/금액 확인 |
| IONE AI | /pages/member/activity/ione_ai.php | [보기](https://leejinho970715-star.github.io/CRM/#ai) | 기록 근거와 우선 고객을 전용 화면에서 확인하고 후속 업무로 연결 |
| 업무일지 | /pages/member/report/work_report.php | [보기](https://leejinho970715-star.github.io/CRM/#work-report) | 활동 내역과 담당자별 일지 메모를 함께 보여주고 선보고 초안 제공 |
| 사용자 정의 보고서 | /pages/member/report/custom_reports.php | [보기](https://leejinho970715-star.github.io/CRM/#custom-reports) | 구성 패널+실시간 집계 결과, 월별 교차 표, 저장한 보고서 불러오기 |
| SSL 기초정보 관리 | /pages/member/contract/ssl_master.php | [보기](https://leejinho970715-star.github.io/CRM/#ssl-master) | 품목·공급사·갱신주기를 같은 관리 규칙의 탭으로 정리 |
| SSL 매입 관리 | /pages/member/contract/ssl_purchase.php | [보기](https://leejinho970715-star.github.io/CRM/#ssl-purchase) | 발주 기본 정보와 품목별 수량·단가·부가세 합계를 한 폼으로 묶기 |
| SSL 출고 관리 | /pages/member/contract/ssl_delivery.php | [보기](https://leejinho970715-star.github.io/CRM/#ssl-delivery) | 설치·출고·도메인·인증서 정보를 고객 맥락과 상세 패널에 연결 |
| SSL 만료·갱신 관리 | /pages/member/contract/ssl_expiration.php | [보기](https://leejinho970715-star.github.io/CRM/#ssl-expiration) | 만료일·잔여일·알림 구간 우선 노출, 갱신 폼과 확인 상태 연결 |
| 포캐스팅 등록 | /pages/member/forecast/forecast_add.php | [보기](https://leejinho970715-star.github.io/CRM/#forecast-add) | 고객·계약/금액·일정/이월 정보로 입력 묶기, 라이선스+교육비 자동 합계 |
| 포캐스팅 현황 | /pages/member/forecast/forecast_status.php | [보기](https://leejinho970715-star.github.io/CRM/#forecast-status) | 반복 월별 표를 한 목록+기간 필터+전체/이월/달성 탭으로 통합 |
| 기타계약 포캐스팅 등록 | /pages/member/other_contract/forecast_add_other.php | [보기](https://leejinho970715-star.github.io/CRM/#other-add) | 포캐스팅과 같은 입력 규칙을 기타계약에 적용 |
| 기타계약 포캐스팅 현황 | /pages/member/other_contract/forecast_status_other.php | [보기](https://leejinho970715-star.github.io/CRM/#other-status) | 계약 예정·이월·달성 현황을 같은 기준으로 비교 |
| 관리자 대시보드 | /pages/admin/dashboard.php | [보기](https://leejinho970715-star.github.io/CRM/#admin) | 계정·조직/기준정보/운영 설정으로 관리자 메뉴를 목적별 분류 |
| 회원·담당업무 관리 | /pages/admin/members.php | [보기](https://leejinho970715-star.github.io/CRM/#members) | 회원 정보·담당 업무·재직 상태를 통합하고 업무별 설정 패널 제공 |
| 고객사 담당자 이관 | /pages/admin/company_sales_rep_transfer.php | [보기](https://leejinho970715-star.github.io/CRM/#transfer) | 대상 고객 선택과 변경 전·후 담당자 비교를 하나의 화면에 배치 |
| 페이지 접근 권한 | /pages/admin/roles.php | [보기](https://leejinho970715-star.github.io/CRM/#permissions) | 역할 선택과 페이지 목록을 같은 권한 설정 흐름으로 정리 |
| 부서 관리 | /pages/admin/departments.php | [보기](https://leejinho970715-star.github.io/CRM/#departments) | 부서와 소속 인원을 표에서 비교, 등록은 필요할 때 열기 |
| 부서 신규 등록 | /pages/admin/department_add.php | [보기](https://leejinho970715-star.github.io/CRM/#department-add) | 부서 등록 후 관리 목록으로 연결 |
| 매출 목표 관리 | /pages/admin/goal/goal_list.php | [보기](https://leejinho970715-star.github.io/CRM/#goals) | 사원별 월 목표 입력과 자동 연간 합계, 연도 전환 제공 |
| 관리항목 관리 | /pages/admin/manage_items.php | [보기](https://leejinho970715-star.github.io/CRM/#manage-items) | 관리 항목 이름과 선택값을 한 입력 화면으로 정리 |
| 기관유형 관리 | /pages/admin/institution_types.php | [보기](https://leejinho970715-star.github.io/CRM/#institutions) | 기관유형별 사용 현황과 선택 항목 관리 |
| 유입정보 관리 | /pages/admin/company_acquisition_options.php | [보기](https://leejinho970715-star.github.io/CRM/#acquisition) | 소스출처·인입경로의 상위 관계를 명확하게 표시 |
| 영리 뉴스 관리 | /pages/admin/commercial_news_keywords.php | [보기](https://leejinho970715-star.github.io/CRM/#commercial-news) | 수집 사용·노출 순서·키워드 구분을 같은 관리 목록으로 정리 |
| 비영리 뉴스 키워드 | /pages/admin/nonprofit_news_keywords.php | [보기](https://leejinho970715-star.github.io/CRM/#nonprofit-keywords) | 기관 설립·예산 키워드와 수집 상태 관리 |
| 품목 관리 | /pages/admin/products.php | [보기](https://leejinho970715-star.github.io/CRM/#products) | 품목명·코드·활성 상태와 옵션 수를 비교 |
| 품목옵션 관리 | /pages/admin/product_options.php | [보기](https://leejinho970715-star.github.io/CRM/#product-options) | 제품별 옵션·코드·활성 상태를 연결 |
| 품목옵션 일괄등록 | /pages/admin/product_options_upload.php | [보기](https://leejinho970715-star.github.io/CRM/#options-upload) | 옵션 파일의 선택·검증·반영 결과를 단계별 제공 |
| 마케팅 활동유형 | /pages/admin/marketing_activity_options.php | [보기](https://leejinho970715-star.github.io/CRM/#marketing-types) | 활동유형의 등록·수정·사용 상태를 같은 목록 규칙으로 관리 |
| 업무일지 운영 설정 | /pages/admin/work_report.php | [보기](https://leejinho970715-star.github.io/CRM/#work-settings) | 업무일지 표시 대상과 선보고 수신 대상을 구분 |
| 시스템·알림 설정 | /pages/admin/settings.php | [보기](https://leejinho970715-star.github.io/CRM/#system) | 브랜드/로그인 이미지 미리보기와 알림 수신 정보를 구분 |
| 데이터 마이그레이션 | /pages/admin/migrate_clients.php | [보기](https://leejinho970715-star.github.io/CRM/#migration) | 원본 미열람: 샘플 중복·필수값 검증만 보여주는 별도 제안 |
| 로그인 | /pages/auth/login/login.php | [보기](https://leejinho970715-star.github.io/CRM/#login) | 브랜드와 인증 영역 분리, 지속 레이블, 찾기·가입 보조 흐름 정리 |
