import asyncio
import httpx

async def fetch_sonarcloud_projects(api_key, organization, page=1, page_size=100):
    url = f'https://sonarcloud.io/api/components/search?organization={organization}&qualifiers=TRK&page={page}&pageSize={page_size}'
    headers = {'Authorization': f'Bearer {api_key}'}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()['components']
    else:
        print(f"Failed to fetch SonarCloud projects. Status code: {response.status_code}")
        return None

async def fetch_all_sonarcloud_projects(api_key, organization):
    all_projects = []
    page = 1

    while True:
        projects = await fetch_sonarcloud_projects(api_key, organization, page)
        if not projects:
            break

        all_projects.extend(projects)
        page += 1

    return all_projects

async def main():
    sonarcloud_api_key = 'YOUR_SONARCLOUD_API_KEY'
    sonarcloud_organization = 'YOUR_ORGANIZATION_KEY'

    projects = await fetch_all_sonarcloud_projects(sonarcloud_api_key, sonarcloud_organization)

    if projects:
        for project in projects:
            print(f"Project: {project['name']} - Key: {project['key']}")

if __name__ == "__main__":
    asyncio.run(main())
